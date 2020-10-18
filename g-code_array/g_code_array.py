def array(original_file, output_file, num_x = 1, dist_x = 1, num_y = 1, dist_y = 1, header_end = "(Start array)"):
    with open(original_file, 'r') as input, open(output_file, 'w') as output:
        lines = input.readlines()
        section_to_copy = ""
        termination_line = "M2"
        coordinate_mode = "absolute"

        for line in lines:
            if "M2" in line:
                # M2 is the g-code signal to end program
                termination_line = line
                break
            if header_end == "":
                section_to_copy += line
            else:
                if header_end in line:
                    header_end = ""
                output.write(line)
            if "G91" in line:
                coordinate_mode = "relative"
        # Only the header should be written at this point.
        # The section_to_copy and termination_line are stored in local memory
        

        # Save the origin (position immediately after header) as S1
        output.write("G60 S1\n\n")

        for x in range(num_x):
            if x > 0:
                output.write(f"G0 X 0{dist_x}\n")
            for y in range(num_y):
                if y > 0:
                    output.write(f"G0 Y 0{dist_y}\n")
                output.write(f"(Copy {x}, {y})\n\n")
                if coordinate_mode == "relative":
                    # Return to origin
                    output.write("G61 XYZ S1\n")
                    output.write(section_to_copy)
                    output.write("\n")
                else:
                    print("Error: Only relative coordinate g-code is supported at this time")
            # Need to return home from the y offsets
            output.write(f"G0 Y-0{(num_y - 1) * dist_y}\n")
        # Return X home from the x offsets
        output.write(f"G0 X-0{(num_x - 1) * dist_x}\n")

        # Need to add the signal to end program back in
        output.write(termination_line)

def select_file():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    print("Select g-code file to array.")
    selected_file = filedialog.askopenfilename()
    print(f"Selected file {selected_file}")
    return selected_file

num_x = int(input("How many horizontal copies?\n"))
dist_x = 0
if num_x > 1:
    dist_x = float(input("How much space between horizontal copies?\n"))
num_y = int(input("How many vertical copies?\n"))
dist_y = 0
if num_y > 1:
    dist_y = float(input("How much space between vertical copies?\n"))
print(f"Will create {num_x} copies horizontally and {num_y} copies vertically.")

print("Select file to array.")
original_file = select_file()
array_file = original_file.split('.')[0] + "_array"
if len(original_file.split('.')) > 1:
    array_file += "." + original_file.split('.')[1]

array(original_file, array_file, num_x, dist_x, num_y, dist_y, "S9000")

print(f"Wrote {array_file}")

input()