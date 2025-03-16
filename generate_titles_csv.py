import csv

# Define 50 AI-generated capstone titles with categories and beneficiaries
titles_data = [
    ["AI-Powered Smart Home Automation", "Artificial Intelligence", "Homeowners"],
    ["Automated Plant Watering System Using IoT", "IoT", "Farmers"],
    ["Smart Traffic Light Control with AI", "Artificial Intelligence", "City Government"],
    ["AI-Based Fire Detection and Prevention", "Safety & Security", "Fire Departments"],
    ["Machine Learning-Based Fraud Detection", "Finance & Security", "Banks"],
    ["Blockchain-Enabled Voting System", "Blockchain", "Government"],
    ["AI-Powered Chatbot for Mental Health", "Healthcare", "Patients & Therapists"],
    ["Smart Waste Management Using IoT", "IoT", "City Waste Management"],
    ["Automated Attendance System with Facial Recognition", "Biometrics", "Schools & Offices"],
    ["AI-Powered Resume Screening System", "Human Resources", "Recruiters"],
    ["AI-Based Early Disease Detection", "Healthcare", "Hospitals"],
    ["Smart Agriculture System with AI Crop Prediction", "Agriculture", "Farmers"],
    ["AI-Driven Disaster Response System", "Emergency Services", "Government"],
    ["AI-Powered Virtual Teacher Assistant", "Education", "Teachers & Students"],
    ["Intelligent Road Accident Detection System", "Safety & Security", "Emergency Responders"],
    ["AI-Based Plagiarism Detection", "Education", "Universities & Students"],
    ["Smart Parking Management with AI", "IoT", "Drivers & Parking Authorities"],
    ["AI-Powered Customer Sentiment Analysis", "Marketing", "Businesses"],
    ["AI-Based Fake News Detection System", "Media & Journalism", "General Public"],
    ["Smart Energy Management for Households", "Energy & Environment", "Homeowners"],
    ["AI-Powered Personalized E-Learning", "Education", "Students"],
    ["AI-Based Traffic Flow Prediction", "Transportation", "City Government"],
    ["AI-Powered Virtual Shopping Assistant", "E-Commerce", "Online Shoppers"],
    ["AI-Based Job Recommendation System", "Career Development", "Job Seekers"],
    ["Smart AI-Enabled Water Quality Monitoring", "Environmental Science", "Communities"],
    ["AI-Powered Healthcare Chatbot", "Healthcare", "Doctors & Patients"],
    ["AI-Based Personalized Music Recommendation", "Entertainment", "Music Lovers"],
    ["Smart Public Transport System with AI", "Transportation", "Commuters"],
    ["AI-Powered Crime Prediction & Prevention", "Security", "Police Departments"],
    ["AI-Based Real-Time Weather Prediction", "Meteorology", "General Public"],
    ["Smart Farming System with AI Pest Detection", "Agriculture", "Farmers"],
    ["AI-Driven Handwritten Text Recognition", "AI & OCR", "Researchers & Archivists"],
    ["AI-Powered Smart Inventory Management", "Retail", "Business Owners"],
    ["AI-Based Personalized Diet & Nutrition Assistant", "Health & Fitness", "Dietitians"],
    ["AI-Enabled Sign Language Translator", "Accessibility", "Hearing Impaired Individuals"],
    ["AI-Powered Virtual Interior Design Assistant", "Design & Architecture", "Homeowners"],
    ["AI-Based Predictive Maintenance for Machines", "Industrial AI", "Manufacturers"],
    ["AI-Powered Smart Grid Energy Optimization", "Energy", "Power Companies"],
    ["AI-Based Language Translation Assistant", "Linguistics", "Travelers & Researchers"],
    ["AI-Powered Personalized Study Planner", "Education", "Students"],
    ["AI-Driven Cybersecurity Threat Detection", "Cybersecurity", "IT Security Teams"],
    ["AI-Powered Automated Essay Grading System", "Education", "Teachers & Schools"],
    ["AI-Based Customer Support Chatbot", "Business", "E-Commerce Stores"],
    ["AI-Powered Smart Office Automation", "IoT", "Corporate Offices"],
    ["AI-Based Financial Risk Assessment", "Finance", "Investors"],
    ["AI-Powered Personalized Workout Planner", "Health & Fitness", "Athletes & Trainers"],
    ["AI-Based Road Traffic Accident Prediction", "Transportation", "Highway Authorities"],
    ["AI-Enabled Real-Time Air Pollution Monitoring", "Environmental Science", "Communities"],
    ["AI-Powered Virtual Shopping Mall", "E-Commerce", "Online Shoppers"],
    
]

# Create a CSV file and save the data
csv_filename = "capstone_titles_dataset.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Category", "Beneficiary"])  # CSV Header
    writer.writerows(titles_data)  # Write the data rows

print(f"CSV file '{csv_filename}' created successfully!")
