import os
import glob
import subprocess

# Define the aim_title dictionary
aim_title = {
    # "1": "Write a program to find the family relation and sum of two numbers.",
    # "2a": "Write a program to find the area and perimeter of a rectangle.",
    # "2b": "Write a program to find the sum, difference, multiplication, division, and integer division.",
    # "3a": "Write a program to find factorial.",
    # "3b": "Write a program to find fibonacci.",
    # "4a": "Write a program to find the GCD and LCM of a given number.",
    # "4b": "Write a program to find the relation.",
    # "4c": "Write a program to find the solution to a tower of Hanoi problem.",
    # "5a": "Write a program to find an area of a triangle.",
    # "5b": "Write a program to find the cube of a given number.",
    # "6a": "Write a program to concatenate.",
    # "6b": "Write a program to delete.",
    # "6c": "Write a program to count the length of a list.",
    # "6d": "Write a program to check whether the given member is in the list or not.",
    # "7a": "Write a program to find the greatest number among given numbers.",
    # "7b": "Write a program to check if the number is a palindrome.",
    # "8a": "Write a program to find the average of a given number.",
    # "8b": "Write a program to find the factor of given number.",
    # "9a": "Write a program to find the relation. (Who is mortal?)",
    # "9b": ". Write a program to find the relation. (Which locations are in Asia ?)"
    # "10a": "Write a program to find the maximum number of given numbers.",
    # "10b": "Write a program to find the greatest number among given number.",
    # "11a": "What are the values of S, M, E, N, D, O, R, and Y that satisfy the equation SEND + MORE = MONEY?",
    # "11b": "Write a program to print a square of stars with a side length X.",
    # "12a": "Write a program to find the path from the start node to the goal node using breadth-first search.",
    # "12b": "Write a program to find the path from the start node to the goal node using depth-first search.",
}


def generate_pdf(title: str, aim: str, question_file: str, output_img: str):
    command = [
        "python3",
        "../main.py",  # Adjust this path to your PDF generator script
        "--title",
        title,
        "--aim",
        aim,
        "--question_file",
        question_file,
        "--output_img",
        output_img,
    ]
    print(f"Generating PDF for {title}...")
    subprocess.run(command)


def main(base_path):
    prolog_files_path = os.path.join(base_path, "prolog", "*.pl")
    images_path = os.path.join(base_path, "img", "*.png")

    # Iterate through each item in the aim_title dictionary
    for key, aim in aim_title.items():
        title = key
        question_file = os.path.join(base_path, "prolog", f"swlab{title}.pl")
        output_img = os.path.join(base_path, "img", f"swlab{title}.png")

        if os.path.exists(question_file) and os.path.exists(output_img):
            generate_pdf(title, aim, question_file, output_img)
        else:
            print(
                f"File not found for {title}: Prolog file: {question_file}, Image file: {output_img}"
            )


if __name__ == "__main__":
    base_path = "/home/rudy/Desktop/untitled/regular/ai"  # Change to your base path
    main(base_path)
