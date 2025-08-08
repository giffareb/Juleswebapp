# Modern POS - Full-Stack Web Application with PromptPay

A complete Point of Sale (POS) web application built with a modern technology stack, featuring a built-in PromptPay QR Code payment system.

## ✨ Tech Stack

*   **Backend:** FastAPI (Python)
*   **Frontend:** SvelteKit & Tailwind CSS
*   **Database:** PostgreSQL
*   **Containerization:** Docker & Docker Compose

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

*   [Install Docker](https://docs.docker.com/get-docker/)
*   [Install Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Running the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Build and run the application with a single command:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for the frontend and backend services, and then start all the containers.

3.  **Access the application:**
    *   **Frontend Application:** Open your browser and navigate to `http://localhost:5173`
    *   **Backend API Docs:** You can access the auto-generated API documentation at `http://localhost:8000/docs`
