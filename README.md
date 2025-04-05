
---

# 🚦 Network Security Detection with MLOps

This project implements an end-to-end **Network Security Detection System** powered by **Machine Learning** and integrated with modern **MLOps practices**. The pipeline covers the full ML lifecycle — from data ingestion to deployment, monitoring, and CI/CD automation.

## 🧠 Overview

The project follows a modular and scalable MLOps architecture with the following stages:

1. **Data Ingestion**:  
   - Source: MongoDB Atlas (cloud-based)
   - Raw data is ingested and stored locally for further processing.

2. **Data Validation & Transformation**:  
   - Schema validation, missing value treatment, data cleaning.
   - Feature engineering and transformation for model compatibility.

3. **Model Training & Selection**:  
   - Multiple ML models are trained and evaluated.
   - Best model is selected based on performance metrics.
   - Model tracking and versioning are done using **MLflow**.

4. **Experiment Tracking**:  
   - Remote tracking using **DagsHub** to monitor logs, metrics, and artifacts.

5. **Batch Prediction**:  
   - A **FastAPI** endpoint is created to perform batch predictions on new incoming data.

6. **Containerization & Deployment**:  
   - Docker image is created for the entire application.
   - Image is stored in **AWS S3** and deployed on **AWS EC2** instance.

7. **CI/CD Pipeline**:  
   - Automated using **GitHub Actions**.
   - Deployment pipeline pushes latest changes to AWS EC2 for production deployment.

---

## 🧰 Tech Stack & Tools

| Category             | Tools/Technologies                                                                 |
|----------------------|-------------------------------------------------------------------------------------|
| Programming Language | Python                                                                             |
| Data Source          | MongoDB Atlas                                                                      |
| ML Lifecycle         | MLflow, Scikit-learn, Pandas, NumPy                                                 |
| API Framework        | FastAPI                                                                            |
| Experiment Tracking  | MLflow, DagsHub                                                                     |
| Version Control      | Git, GitHub                                                                         |
| CI/CD                | GitHub Actions, AWS EC2                                                             |
| Containerization     | Docker                                                                             |
| Cloud Storage        | AWS S3, AWS EC2                                                                    |
| MLOps                | Docker, MLflow, DagsHub, GitHub Actions                                             |

---

## 🚀 How to Run the Project

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/network-security-detection-with-mlops.git
   cd network-security-detection-with-mlops
   ```

2. **Install dependencies**  
   Make sure you have Python 3.8+ and pip installed.
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the project**
   ```bash
   python app.py
   ```

4. **Access the API**
   The FastAPI app will start locally at:  
   `http://127.0.0.1:8000`

---

## 📦 Deployment Instructions

- Dockerize the application:
  ```bash
  docker build -t network-security-detection-app .
  ```

- Push image to AWS S3 and deploy on EC2 instance.

- CI/CD is handled via GitHub Actions. On every push to the main branch, the pipeline:
  - Runs tests
  - Builds Docker image
  - Deploys to EC2

---

## 📈 DagsHub Repository Link

- DagsHub Repo: `https://dagshub.com/atharvmohanjadhav/Network-Security`

---

## 🧑‍💻 Author

**Atharv Mohan Jadhav**  
Connect with me on [GitHub](https://github.com/atharvmohanjadhav)

---
