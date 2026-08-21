# 🔒 Network Security ML Project

[![Python](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange.svg)](https://mlflow.org/)
[![Render](https://img.shields.io/badge/Render-Deployed-purple.svg)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end MLOps project for detecting phishing and malicious URLs using machine learning. This project includes a complete data pipeline, model training with MLflow tracking, and a FastAPI-based prediction service.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Model Training](#model-training)
- [API Endpoints](#api-endpoints)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project implements a complete MLOps pipeline for network security threat detection. It classifies URLs as **phishing/malicious** or **safe/legitimate** using a Random Forest classifier trained on 30 URL features.

### Key Features:
- ✅ End-to-end ML pipeline (Data Ingestion → Validation → Transformation → Training)
- ✅ MLflow + DagsHub experiment tracking
- ✅ FastAPI REST API for predictions
- ✅ HTML results dashboard
- ✅ Docker containerization
- ✅ Deployed on EC2/Render

---

## Features

### 🔄 Data Pipeline
- MongoDB data ingestion
- Data validation with schema checking
- Data drift detection
- KNN imputation for missing values
- Train-test split

### 🤖 Model Training
- Multiple models tested (Random Forest, Gradient Boosting, Logistic Regression, AdaBoost, Decision Tree)
- Hyperparameter tuning with cross-validation
- MLflow experiment tracking
- DagsHub integration for model registry

### 🌐 API Service
- **FastAPI** web server
- **CSV upload** for batch predictions
- **HTML results** with summary statistics
- **File saving** on server with timestamps
- **Swagger UI** for API documentation
- **Health check** endpoint

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.8 |
| **Web Framework** | FastAPI, Uvicorn |
| **ML Libraries** | scikit-learn, pandas, numpy |
| **Experiment Tracking** | MLflow, DagsHub |
| **Database** | MongoDB |
| **Containerization** | Docker |
| **Deployment** | AWS EC2, Render |
| **Frontend** | Jinja2 Templates, Bootstrap |

---


### Feature Descriptions

| # | Feature Name | Description | Values |
|---|--------------|-------------|--------|
| 1 | **having_IP_Address** | URL has IP address instead of domain | 1 = Yes, -1 = No, 0 = Unknown |
| 2 | **URL_Length** | Length of the URL | 1 = Long (>54), -1 = Short, 0 = Unknown |
| 3 | **Shortining_Service** | Uses URL shortener (bit.ly, goo.gl) | 1 = Yes, -1 = No, 0 = Unknown |
| 4 | **having_At_Symbol** | Has @ symbol in URL | 1 = Yes, -1 = No, 0 = Unknown |
| 5 | **double_slash_redirecting** | Has // in URL path | 1 = Yes, -1 = No, 0 = Unknown |
| 6 | **Prefix_Suffix** | Has dash (-) in domain | 1 = Yes, -1 = No, 0 = Unknown |
| 7 | **having_Sub_Domain** | Has multiple subdomains | 1 = Yes, -1 = No, 0 = Unknown |
| 8 | **SSLfinal_State** | SSL certificate status | 1 = Valid SSL, -1 = No/Invalid SSL, 0 = Unknown |
| 9 | **Domain_registeration_length** | Domain age | 1 = >6 months, -1 = <6 months, 0 = Unknown |
| 10 | **Favicon** | Favicon source | 1 = External domain, -1 = Same domain, 0 = Unknown |
| 11 | **port** | Port number used | 1 = Non-standard, -1 = Standard, 0 = Unknown |
| 12 | **HTTPS_token** | Has "https" token | 1 = Yes, -1 = No, 0 = Unknown |
| 13 | **Request_URL** | External object requests | 1 = External, -1 = Same domain, 0 = Unknown |
| 14 | **URL_of_Anchor** | External anchor links | 1 = External, -1 = Same domain, 0 = Unknown |
| 15 | **Links_in_tags** | External meta/link tags | 1 = External, -1 = Same domain, 0 = Unknown |
| 16 | **SFH** | Server Form Handler | 1 = External, -1 = Same domain, 0 = Unknown |
| 17 | **Submitting_to_email** | Form submits to email | 1 = Yes, -1 = No, 0 = Unknown |
| 18 | **Abnormal_URL** | Abnormal URL structure | 1 = Yes, -1 = No, 0 = Unknown |
| 19 | **Redirect** | Multiple redirects | 1 = Yes, -1 = No, 0 = Unknown |
| 20 | **on_mouseover** | Hover hides URL | 1 = Yes, -1 = No, 0 = Unknown |
| 21 | **RightClick** | Right-click disabled | 1 = Yes, -1 = No, 0 = Unknown |
| 22 | **popUpWidnow** | Pop-ups detected | 1 = Yes, -1 = No, 0 = Unknown |
| 23 | **Iframe** | Uses iframes | 1 = Yes, -1 = No, 0 = Unknown |
| 24 | **age_of_domain** | Domain age | 1 = >6 months, -1 = <6 months, 0 = Unknown |
| 25 | **DNSRecord** | DNS record exists | 1 = Yes, -1 = No, 0 = Unknown |
| 26 | **web_traffic** | Web traffic ranking | 1 = High, -1 = Low, 0 = Unknown |
| 27 | **Page_Rank** | Google PageRank | 1 = High, -1 = Low, 0 = Unknown |
| 28 | **Google_Index** | Indexed by Google | 1 = Yes, -1 = No, 0 = Unknown |
| 29 | **Links_pointing_to_page** | Incoming links count | 1 = High, -1 = Low, 0 = Unknown |
| 30 | **Statistical_report** | Statistical risk | 1 = Low risk, -1 = High risk, 0 = Unknown |

### Quick Reference: What the Values Mean

| Value | Meaning |
|-------|---------|
| **1** | Suspicious / Yes / Present / Phishing indicator |
| **-1** | Normal / No / Safe indicator |
| **0** | Unknown / Neutral / Not applicable |


---




