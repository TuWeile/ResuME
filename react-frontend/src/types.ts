// src/types.ts
export interface Address {
    street: string;
    city: string;
    state: string;
    zip: string;
    country: string;
  }
  
  export interface PersonalInfo {
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    address: Address;
    date_of_birth: string; // Using string to represent ISO date format
  }
  
  export interface Experience {
    company: string;
    position: string;
    start_date: string; // Using string to represent ISO date format
    end_date?: string; // Using string to represent ISO date format
    responsibilities: string;
    details?: string;
  }
  
  export interface Education {
    institution: string;
    degree: string;
    major: string;
    minor?: string;
    gpa?: number;
    max_gpa?: number;
    honours?: string;
    start_date: string; // Using string to represent ISO date format
    end_date?: string; // Using string to represent ISO date format
    details?: string;
  }
  
  export interface Project {
    name: string;
    description: string;
    technologies: string[];
    role: string;
    url?: string;
    start_date: string; // Using string to represent ISO date format
    end_date?: string; // Using string to represent ISO date format
  }
  
  export interface Certification {
    title: string;
    achievement: string;
    date: string; // Using string to represent ISO date format
  }
  
  export interface Attachment {
    type: string;
    file_name: string;
    file_url: string;
    uploaded_at: string; // Using string to represent ISO date format
  }
  
  export interface Behavioural {
    question: string;
    answer: string;
  }
  
  export interface User {
    id: string;
    personal_info: PersonalInfo;
    experiences?: Experience[];
    educations?: Education[];
    projects?: Project[];
    certifications?: Certification[];
    biography?: string;
    motivations?: string;
    strengths?: string;
    weaknesses?: string;
    attachments?: Attachment[];
    linkedin?: string;
    website?: string;
    behavioural?: Behavioural[];
    skills?: string;
    created_at: number;
    deleted_by: number;
  }
  
  export interface UserUpdateSearch {
    personal_info?: PersonalInfo;
    experiences?: Experience[];
    educations?: Education[];
    projects?: Project[];
    certifications?: Certification[];
    biography?: string;
    motivations?: string;
    strengths?: string;
    weaknesses?: string;
    attachments?: Attachment[];
    linkedin?: string;
    website?: string;
    behavioural?: Behavioural[];
    skills?: string;
  }
  