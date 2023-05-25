from django.shortcuts import render, HttpResponse
from pyresparser import ResumeParser
from Home.models import DemoModel

def SignupPage(request):
    return render(request,'signup.html')

def LoginPage(request):
    return render(request,'login.html')


def resume_view(request):
    # retrieve data from database
    # demo_data = DemoModel.objects.all().latest()
    demo_data = DemoModel.objects.all().latest('id')

    # pass data to template context
    context = {
        'name': demo_data.name,
        'email': demo_data.email,
        'phone': demo_data.phone,
        'career_summary': demo_data.career_summary,
        'skills': demo_data.skills,
        'work_experience': demo_data.work_experience,
        'eductional_summary': demo_data.eductional_summary,
        'certification': demo_data.certification,
        'personal_details': demo_data.personal_details,
        'declaration': demo_data.declaration,
    }
    return render(request, 'resume.html', context=context)

def doc_resume_view(request):
    # retrieve data from database
    # demo_data = DemoModel.objects.all().latest()
    demo_data = DemoModel.objects.all().latest('id')

    # pass data to template context
    context = {
        'name': demo_data.name,
        'email': demo_data.email,
        'phone': demo_data.phone,
        'career_summary': demo_data.career_summary,
        'skills': demo_data.skills,
        'work_experience': demo_data.work_experience,
        'eductional_summary': demo_data.eductional_summary,
        'certification': demo_data.certification,
        'personal_details': demo_data.personal_details,
        'declaration': demo_data.declaration,
    }
    return render(request, 'docresume.html',context=context)

import tempfile
import os
def upload_file(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            # Get the uploaded file from the request
            uploaded_file = request.FILES['file']
            # Save the file to a temporary file on disk
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(uploaded_file.read())
                file_path = f.name       

            # Extract additional data using pyresparser   
            print(file_path) 
            # resume_data = ResumeParser(file_path).get_extracted_data()  
           
            # Determine the file type by examining the file extension
            # file_extension = uploaded_file.name.split('.')[-1]   
            file_extension = os.path.splitext(uploaded_file.name)[1][1:].lower()

            # Call the appropriate function based on the file type
            if file_extension == 'pdf':
                extracted_data = extract_pdf_data(file_path)
            elif file_extension == 'doc' or file_extension == 'docx':
                extracted_data = extract_word_data(file_path)
            elif file_extension == 'txt':
                extracted_data = extract_text_data(file_path)
            else:
                return HttpResponse('Unsupported file type') 
            # Write the extracted data to a new text file
            with open('extracted_data.txt', 'w', encoding='utf-8') as f:
                f.write(extracted_data)      
            # Do something with the extracted data
            # print(extracted_data)        
            
            valid_email = validate_emails(extracted_data)
            if valid_email:
                print(f"The valid email address is {valid_email}")
            else:
                print("No valid email address found")

            valid_phone_number = validate_phone_numbers(extracted_data)
            if valid_phone_number:
                print(f"The valid phone number is {valid_phone_number}")
            else:
                print("No valid phone number found") 
    
            # calling extract_name_from_resume function
            name=extract_name_from_resume(extracted_data)
            print(name)   

            headings_and_content = differentiate_headings_and_content(extracted_data)
            headings_and_content['NAME']=name
            headings_and_content['EMAIL']= valid_email
            headings_and_content['CONTACT']= valid_phone_number

            # # Extract additional data using pyresparser
            # # resume_data = ResumeParser.resume(file_path).get_extracted_data()
            
            # # Access the extracted information
            # name = resume_data.get('name', '')
            # email = resume_data.get('email', '')
            # phone = resume_data.get('mobile_number', '')
            # skills = resume_data.get('skills', [])
            # experience = resume_data.get('experience', [])
            # education = resume_data.get('education', [])
            
            # # Print the extracted information
            # print("Name:", name)
            # print("Email:", email)
            # print("Phone:", phone)
            # print("Skills:", skills)
            # print("Experience:", experience)
            # print("Education:", education)            

            # creating model/database instance
            ins = DemoModel(name=name,
                    email=valid_email,
                    phone=valid_phone_number,
                    career_summary=headings_and_content.get("CAREER_OBJECTIVE", ""),
                    skills=headings_and_content.get("SKILLS", ""),
                    work_experience=headings_and_content.get("EXPERIENCE", ""),
                    eductional_summary=headings_and_content.get("EDUCATION", ""),
                    certification=headings_and_content.get("CERTIFICATION", ""),
                    personal_details=headings_and_content.get("", ""),
                    declaration=headings_and_content.get("DECLARATION", ""))

            ins.save() 

        return render(request, "selectformat.html")
    # If the request method is not POST, render the file upload form
    return render(request, 'upload.html')

            # # extracting some data from uploaded file using pyresparser
            # pyredata = ResumeParser.resume(file_path).get_extracted_data()


            # print("Name:", pyredata['name'])
            # print("Email:", pyredata['email'])
            # print("Mobile Number:", pyredata['mobile_number'])
            # print("Skills:", pyredata['skills'])
            # print("Experience:", pyredata['experience'])
            # print("College Name:", pyredata['college_name'])


# def resume_view(request):
#     # retrieve data from database
#     # demo_data = DemoModel.objects.all().latest()
#     demo_data = DemoModel.objects.all().latest('id')

#     # pass data to template context
#     context = {
#         'name': demo_data.name,
#         'email': demo_data.email,
#         'phone': demo_data.phone,
#         'career_summary': demo_data.career_summary,
#         'skills': demo_data.skills,
#         'work_experience': demo_data.work_experience,
#         'eductional_summary': demo_data.eductional_summary,
#         'certification': demo_data.certification,
#         'personal_details': demo_data.personal_details,
#         'declaration': demo_data.declaration,
#     }

#     print(demo_data)


#     # render template with context
#     return render(request, 'selectformat.html', context=context)

import fitz
import tabula

def extract_pdf_data(uploaded_file):
    # Open the PDF file
    with fitz.open(uploaded_file) as pdf:
        text_pages = []
        # Iterate over pages
        for page in pdf:
            # Extract the text from the page
            text = page.get_text("text")
            # Append to list of text pages
            text_pages.append(text)
        # Join text pages with line breaks
        full_text = "\n".join(text_pages)
        # Extract tables from PDF
        dfs = tabula.read_pdf(uploaded_file, pages='all')
        # Append tables to full_text
        for i in range(len(dfs)):
            full_text += '\n\n' + str(dfs[i])
        # Return the extracted text and tables
        return full_text

import docx
def extract_word_data(file_path):
    document = docx.Document(file_path)
    data = []
    for paragraph in document.paragraphs:
        data.append(paragraph.text)
    return "\n".join(data)


def extract_text_data(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    return data


import re
def validate_emails(extracted_data):
    # Define a regular expression pattern to match email addresses
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    # Find all the email addresses in the extracted data
    emails = email_pattern.findall(extracted_data)
    # If there is at least one email address, return the first one
    if emails:
        return emails[0]
    # If there are no email addresses, return None
    return None


def validate_phone_numbers(extracted_data):
    # Define a regular expression pattern to match phone numbers
    phone_pattern = re.compile(r'(\d{10})')
    # Find all the phone numbers in the extracted data
    phone_numbers = phone_pattern.findall(extracted_data)
    # If there is at least one phone number, return the first one
    if phone_numbers:
        return phone_numbers[0]
    # If there are no phone numbers, return None
    return None

#TO EXTRACT NAME FROM RESUME
import spacy
# nlp = spacy.load("en_core_web_sm")
def extract_name_from_resume(extracted_data):
    # with open(extracted_data, 'r') as file:
    #     text = file.read()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(extracted_data)
    names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names.append(ent.text)
    return names[0]

# old fun 
def differentiate_headings_and_content(resume_text):
    # Load the pre-trained English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the resume text
    doc = nlp(resume_text)

    # Initialize variables to store the current heading and its content
    current_heading = None
    current_content = ""

    # Initialize a dictionary to store the identified headings and their content
    headings_and_content = {}

    # Define the set of headings
    headings = {
        "EDUCATION": ["education","academic background","educational qualifications","educational history",
                      "academic achievements","academic credentials","education and training","educational experience",
                      "academic record","formal education","educational highlights","educational background",
                      "degrees and certifications","educational attainment","professional education","academic profile",
                      "relevant education","education and degrees","educational accomplishments","academic training",
                      "qualifications and education"],

        "SKILLS": ["skills","core competencies","key skills","technical proficiencies","areas of expertise",
                   "technical skills","software proficiencies","specialized skills","qualifications",
                   "strengthsskillset","professional skills","language proficiencies","industry knowledge",
                   "tools and technologies","functional skills","interpersonal skills","leadership skills",
                   "transferable skills","relevant skills"],

        "EXTRA_CURRICULAR": ["extra-curricular", "activities","activities and involvement","leadership experience",
                             "volunteering and community engagement","community service","professional development",
                             "skills and interests","relevant hobbies","additional engagements","special projects",
                             "personal initiatives","non-academic pursuits","club memberships","campus involvement",
                             "team memberships","creative pursuits","athletics and sports","social and cultural activities",
                             "philanthropy and fundraising","entrepreneurial ventures","professional affiliations","undertaken projects"],

        "CERTIFICATION": ["certification","professional certifications","certification highlights","certified achievements",
                          "credentialing","certifications and licenses","industry certifications","certification portfolio",
                          "certified expertise","certified skills","certification credentials","professional designations",
                          "certification accomplishments","certification training","certified proficiencies",
                          "certified specializations","accredited certifications","industry-recognized certifications",
                          "professional licenses","certified training and development","validated certifications",
                          "extra-curricular activities & certification "],

        "EXPERIENCE" : ["experience","experiences"],

        "CAREER_OBJECTIVE": ["career", "objective", "career objective", "career", "objective","professional summary",
                             "career summary","profile","career profile","professional profile","overview",
                             "summary of qualifications","key skills and experience","career highlights",
                             "career goals","personal statement","value proposition","core competencies",
                             "skills summary","expertise summary","career focus","career objectives",
                             "professional goals","introduction"],

        "DECLARATION": ["declaration","professional affirmation","personal statement","commitment statement",
                        "career pledge","ethical declaration","statement of integrity","career promise",
                        "professional vow","professional code","career commitment","statement of professionalism",
                        "values statement","professional oath","professional assurance","career dedication",
                        "ethical pledge","personal integrity statement","career ethics statement","career mission statement",
                        "professional conduct statement","activities","Activities"]
    }

    # Iterate over each sentence in the resume
    for sentence in doc.sents:
        # Convert the sentence to lowercase for easier matching
        sentence_text = sentence.text.lower()

        # Check if the sentence matches any of the headings
        for heading, keywords in headings.items():
            if any(keyword in sentence_text for keyword in keywords):
                # If a new heading is encountered, store the previous heading and its content (if any)
                if current_heading:
                    if current_heading not in headings_and_content:
                        headings_and_content[current_heading] = []
                    headings_and_content[current_heading].append(current_content.strip())
                current_heading = heading
                current_content = ""
                break

        # If a heading has been identified, add the sentence to its content
        if current_heading:
            current_content += sentence.text + " "

    # Add the last heading and its content to the dictionary
    if current_heading:
        if current_heading not in headings_and_content:
            headings_and_content[current_heading] = []
        headings_and_content[current_heading].append(current_content.strip())

    # Clean the extracted content
    for heading, content in headings_and_content.items():
        if isinstance(content, str):
            headings_and_content[heading] = clean_data([content])[0]
        elif isinstance(content, list):
            headings_and_content[heading] = clean_data(content)[0]    

    # Format the extracted content
        # for heading, content in headings_and_content.items():
        #     if isinstance(content, str):
        #         headings_and_content[heading] = format_data(content)
        #     elif isinstance(content, list):
        #         formatted_list = []
        #         for item in content:
        #             formatted_list.append(format_data(item))
        #         headings_and_content[heading] = formatted_list   
        #------------------------------------------------------------------------
        # for heading, content in headings_and_content.items():
        #     if isinstance(content, str):
        #         print("Original Content:", content)  # Print the original content
        #         headings_and_content[heading] = format_data(content)
        #         print("Formatted Content:", headings_and_content[heading])  # Print the formatted content
        #     elif isinstance(content, list):
        #         formatted_list = []
        #         for item in content:
        #             print("Original Content:", item)  # Print the original content
        #             formatted_list.append(format_data(item))
        #             print("Formatted Content:", formatted_list[-1])  # Print the formatted content
        #         headings_and_content[heading] = formatted_list
     

    return headings_and_content

# def differentiate_headings_and_content(resume_text):
    # Load the pre-trained English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the resume text
    doc = nlp(resume_text)

    # Initialize variables to store the current heading and its content
    current_heading = None
    current_content = ""

    # Initialize a dictionary to store the identified headings and their content
    headings_and_content = {}

    # Define the set of headings
    headings = {
        "EDUCATION": ["education","academic background","educational qualifications","educational history",
                      "academic achievements","academic credentials","education and training","educational experience",
                      "academic record","formal education","educational highlights","educational background",
                      "degrees and certifications","educational attainment","professional education","academic profile",
                      "relevant education","education and degrees","educational accomplishments","academic training",
                      "qualifications and education"],

        "SKILLS": ["skills","core competencies","key skills","technical proficiencies","areas of expertise",
                   "technical skills","software proficiencies","specialized skills","qualifications",
                   "strengthsskillset","professional skills","language proficiencies","industry knowledge",
                   "tools and technologies","functional skills","interpersonal skills","leadership skills",
                   "transferable skills","relevant skills"],

        "EXTRA_CURRICULAR": ["extra-curricular", "activities","activities and involvement","leadership experience",
                             "volunteering and community engagement","community service","professional development",
                             "skills and interests","relevant hobbies","additional engagements","special projects",
                             "personal initiatives","non-academic pursuits","club memberships","campus involvement",
                             "team memberships","creative pursuits","athletics and sports","social and cultural activities",
                             "philanthropy and fundraising","entrepreneurial ventures","professional affiliations"],

        "CERTIFICATION": ["certification","professional certifications","certification highlights","certified achievements",
                          "credentialing","certifications and licenses","industry certifications","certification portfolio",
                          "certified expertise","certified skills","certification credentials","professional designations",
                          "certification accomplishments","certification training","certified proficiencies",
                          "certified specializations","accredited certifications","industry-recognized certifications",
                          "professional licenses","certified training and development","validated certifications"],

        "EXPERIENCE" : ["experience","experiences"],

        "CAREER_OBJECTIVE": ["career", "objective", "career objective", "career", "objective","professional summary",
                             "career summary","profile","career profile","professional profile","overview",
                             "summary of qualifications","key skills and experience","career highlights",
                             "career goals","personal statement","value proposition","core competencies",
                             "skills summary","expertise summary","career focus","career objectives",
                             "professional goals","introduction"],

        "DECLARATION": ["declaration","professional affirmation","personal statement","commitment statement",
                        "career pledge","ethical declaration","statement of integrity","career promise",
                        "professional vow","professional code","career commitment","statement of professionalism",
                        "values statement","professional oath","professional assurance","career dedication",
                        "ethical pledge","personal integrity statement","career ethics statement","career mission statement",
                        "professional conduct statement","activities","Activities"]
    }

    # Iterate over each sentence in the resume
    for sentence in doc.sents:
        # Convert the sentence to lowercase for easier matching
        sentence_text = sentence.text.lower()

        # Check if the sentence matches any of the headings
        matched_heading = None
        for heading, keywords in headings.items():
            if any(keyword in sentence_text for keyword in keywords):
                matched_heading = heading
                break

        # If a new heading is encountered, store the previous heading and its content (if any)
        if matched_heading:
            if current_heading and current_content:
                if current_heading not in headings_and_content:
                    headings_and_content[current_heading] = []
                headings_and_content[current_heading].append(current_content.strip())
            current_heading = matched_heading
            current_content = ""

        # Add the sentence to the content of the current heading
        if current_heading:
            current_content += sentence.text + " "

        # Handle "Skills" and "Activities" headings separately
        if matched_heading == "SKILLS":
            if "activities" in sentence_text:
                if current_heading and current_content:
                    if current_heading not in headings_and_content:
                        headings_and_content[current_heading] = []
                    headings_and_content[current_heading].append(current_content.strip())
                current_heading = "DECLARATION"
                current_content = sentence.text + " "
            else:
                current_heading = matched_heading
                current_content += sentence.text + " "
        elif matched_heading == "DECLARATION":
            current_heading = matched_heading
            current_content += sentence.text + " "
        else:
            if current_heading and current_content:
                if current_heading not in headings_and_content:
                    headings_and_content[current_heading] = []
                headings_and_content[current_heading].append(current_content.strip())
            current_heading = matched_heading
            current_content = sentence.text + " "

    # Add the last heading and its content to the dictionary
    if current_heading and current_content:
        if current_heading not in headings_and_content:
            headings_and_content[current_heading] = []
        headings_and_content[current_heading].append(current_content.strip())

    # Clean the extracted content
    for heading, content in headings_and_content.items():
        if isinstance(content, str):
            headings_and_content[heading] = clean_data([content])[0]
        elif isinstance(content, list):
            headings_and_content[heading] = clean_data(content)[0]

    return headings_and_content

# seperate code snippet for identifying Skills and Activities
# def differentiate_headings_and_content(resume_text):
    # Load the pre-trained English language model
    nlp = spacy.load("en_core_web_sm")

    # Process the resume text
    doc = nlp(resume_text)

    # Initialize variables to store the current heading and its content
    current_heading = None
    current_content = ""

    # Initialize a dictionary to store the identified headings and their content
    headings_and_content = {}

    # Define the set of headings
    headings = {
        "EDUCATION": ["education","academic background","educational qualifications","educational history",
                      "academic achievements","academic credentials","education and training","educational experience",
                      "academic record","formal education","educational highlights","educational background",
                      "degrees and certifications","educational attainment","professional education","academic profile",
                      "relevant education","education and degrees","educational accomplishments","academic training",
                      "qualifications and education"],

        "SKILLS": ["skills","core competencies","key skills","technical proficiencies","areas of expertise",
                   "technical skills","software proficiencies","specialized skills","qualifications",
                   "strengthsskillset","professional skills","language proficiencies","industry knowledge",
                   "tools and technologies","functional skills","interpersonal skills","leadership skills",
                   "transferable skills","relevant skills"],

        "EXTRA_CURRICULAR": ["extra-curricular", "activities","activities and involvement","leadership experience",
                             "volunteering and community engagement","community service","professional development",
                             "skills and interests","relevant hobbies","additional engagements","special projects",
                             "personal initiatives","non-academic pursuits","club memberships","campus involvement",
                             "team memberships","creative pursuits","athletics and sports","social and cultural activities",
                             "philanthropy and fundraising","entrepreneurial ventures","professional affiliations"],

        "CERTIFICATION": ["certification","professional certifications","certification highlights","certified achievements",
                          "credentialing","certifications and licenses","industry certifications","certification portfolio",
                          "certified expertise","certified skills","certification credentials","professional designations",
                          "certification accomplishments","certification training","certified proficiencies",
                          "certified specializations","accredited certifications","industry-recognized certifications",
                          "professional licenses","certified training and development","validated certifications"],

        "EXPERIENCE" : ["experience","experiences"],

        "CAREER_OBJECTIVE": ["career", "objective", "career objective", "career", "objective","professional summary",
                             "career summary","profile","career profile","professional profile","overview",
                             "summary of qualifications","key skills and experience","career highlights",
                             "career goals","personal statement","value proposition","core competencies",
                             "skills summary","expertise summary","career focus","career objectives",
                             "professional goals","introduction"],

        "DECLARATION": ["declaration","professional affirmation","personal statement","commitment statement",
                        "career pledge","ethical declaration","statement of integrity","career promise",
                        "professional vow","professional code","career commitment","statement of professionalism",
                        "values statement","professional oath","professional assurance","career dedication",
                        "ethical pledge","personal integrity statement","career ethics statement","career mission statement",
                        "professional conduct statement","activities","Activities"]
    }

    # Iterate over each sentence in the resume
    for sentence in doc.sents:
        # Convert the sentence to lowercase for easier matching
        sentence_text = sentence.text.lower()

        # Check if the sentence matches any of the headings
        matched_heading = None
        for heading, keywords in headings.items():
            if any(keyword in sentence_text for keyword in keywords):
                matched_heading = heading
                break

        # If a new heading is encountered, store the previous heading and its content (if any)
        if matched_heading:
            if current_heading and current_content:
                if current_heading not in headings_and_content:
                    headings_and_content[current_heading] = []
                headings_and_content[current_heading].append(current_content.strip())
            current_heading = matched_heading
            current_content = ""

        # Add the sentence to the content of the current heading
        if current_heading:
            current_content += sentence.text + " "

        # Handle "Skills" and "Activities" headings separately
        if matched_heading == "SKILLS":
            if "activities" in sentence_text:
                if current_heading and current_content:
                    if current_heading not in headings_and_content:
                        headings_and_content[current_heading] = []
                    headings_and_content[current_heading].append(current_content.strip())
                current_heading = matched_heading
                current_content = sentence.text + " "
            else:
                if current_heading and current_content:
                    if current_heading not in headings_and_content:
                        headings_and_content[current_heading] = []
                    headings_and_content[current_heading].append(current_content.strip())
                current_heading = matched_heading
                current_content += sentence.text + " "
        elif matched_heading == "DECLARATION":
            if current_heading and current_content:
                if current_heading not in headings_and_content:
                    headings_and_content[current_heading] = []
                headings_and_content[current_heading].append(current_content.strip())
            current_heading = matched_heading
            current_content += sentence.text + " "
        else:
            if current_heading and current_content:
                if current_heading not in headings_and_content:
                    headings_and_content[current_heading] = []
                headings_and_content[current_heading].append(current_content.strip())
            current_heading = matched_heading
            current_content += sentence.text + " "


    # Add the last heading and its content to the dictionary
    if current_heading and current_content:
        if current_heading not in headings_and_content:
            headings_and_content[current_heading] = []
        headings_and_content[current_heading].append(current_content.strip())


    # Clean the extracted content
    for heading, content in headings_and_content.items():
        if isinstance(content, str):
            headings_and_content[heading] = clean_data([content])[0]
        elif isinstance(content, list):
            headings_and_content[heading] = clean_data(content)[0]     

    return headings_and_content




# Function to clean data
def clean_data(data):
    cleaned_data = []
    for entry in data:
        entry = entry.replace('\uf0b7', '')  # Remove unwanted characters
        entry = entry.replace('\uf0d8', '')  # Remove unwanted characters
        entry = entry.replace('\n', ' ')  # Remove newline characters
        entry = entry.strip()  # Remove leading/trailing whitespaces
        if entry.startswith('[') and entry.endswith(']'):  # Remove square brackets
            entry = entry[1:-1].strip()
        cleaned_data.append(entry)
    return cleaned_data    

# import re

# def format_data(data):
#     # Regular expression pattern to identify bullet points
#     bullet_point_pattern = r'(\s*•\s+)'

#     # Split the data into lines
#     lines = data.splitlines()

#     formatted_lines = []
#     for line in lines:
#         # Check if the line starts with a bullet point
#         if re.match(bullet_point_pattern, line):
#             # Add a new line before the bullet point
#             formatted_lines.append('\n' + line)
#         else:
#             # Add the line as is
#             formatted_lines.append(line)

#     # Join the lines back into a single string
#     formatted_data = '\n'.join(formatted_lines)
#     return formatted_data

