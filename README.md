# Snap Class - Face Recognition System

## About the Project

Snap Class is a face recognition system developed as an academic Information Technology project.

The project demonstrates software development, face recognition, database integration, and a graphical user interface to create a practical technology solution.

## Features

- Face recognition
- Face data processing
- Database integration
- Graphical user interface (GUI)
- Image-based recognition
- Multiple application modes

## Technologies

- Python
- OpenCV — camera access and image processing
- face_recognition — face recognition
- cvzone — visual interface elements
- NumPy — numerical operations
- SQLite — student attendance database
- Pickle — loading saved face encodings

## Project Structure

```text
snap-class-face-recognition/
├── main.py
├── add to database.py
├── encoded file.py
├── encoded generator.py
└── resources/
    ├── background.png
    └── modes/
        ├── one.png
        ├── two.png
        ├── three.png
        └── four.png
Academic Project

This project was developed as part of my Diploma in Information Technology (Software Development) at Vaal University of Technology.

Author

Oscar Mhlongo

IT Graduate | Software Development | Networking | CompTIA Network+ Certified

Built as part of my journey in software development and technology.


## Installation and Setup

### Requirements

- Python
- A webcam
- Git

### Install Dependencies

Clone the repository:

```bash
git clone https://github.com/Oscar-Mhlongo-IT/snap-class-face-recognition.git
cd snap-class-face-recognition
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Running the Application

Ensure the required database and face-encoding files are available locally and that the resource image paths match the code.

Run the application:

```bash
python main.py
```

Press `q` to quit the application.

**Note:** The database and face-encoding files are not included in this repository. You must generate or configure them locally before running the application.
