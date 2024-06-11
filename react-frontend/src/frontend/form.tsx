// src/MultiStepForm.tsx
import React, { useState } from 'react';
import { PersonalInfo, Experience, Education, Project, Certification } from '../types';
import './form.css';

interface MultiStepFormProps {
    onComplete: () => void;
}

const MultiStepForm: React.FC<MultiStepFormProps> = ({ onComplete }) => {
    const [step, setStep] = useState(0);
    const [personalInfo, setPersonalInfo] = useState<Partial<PersonalInfo>>({});
    const [experience, setExperience] = useState<Partial<Experience>>({});
    const [education, setEducation] = useState<Partial<Education>>({});
    const [project, setProject] = useState<Partial<Project>>({});
    const [certification, setCertification] = useState<Partial<Certification>>({});

    const handleNext = () => {
        if (step < 5) {
            setStep(step + 1);
        } else {
            onComplete();
        }
    };

    const renderStepContent = () => {
        switch (step) {
            case 0:
                return (
                    <div className="form-step fade-in">
                        <h2>Welcome to ResuME!</h2>
                        <p>Please click "Next" to begin.</p>
                    </div>
                );
            case 1:
                return (
                    <div className="form-step fade-in">
                        <h2>Personal Information</h2>
                        <input
                            type="text"
                            placeholder="First Name"
                            value={personalInfo.first_name || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, first_name: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Last Name"
                            value={personalInfo.last_name || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, last_name: e.target.value })}
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={personalInfo.email || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, email: e.target.value })}
                        />
                        <input
                            type="tel"
                            placeholder="Phone"
                            value={personalInfo.phone || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, phone: e.target.value })}
                        />
                    </div>
                );
            case 2:
                return (
                    <div className="form-step fade-in">
                        <h2>Experience</h2>
                        <input
                            type="text"
                            placeholder="Company"
                            value={experience.company || ''}
                            onChange={(e) => setExperience({ ...experience, company: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Position"
                            value={experience.position || ''}
                            onChange={(e) => setExperience({ ...experience, position: e.target.value })}
                        />
                    </div>
                );
            case 3:
                return (
                    <div className="form-step fade-in">
                        <h2>Education</h2>
                        <input
                            type="text"
                            placeholder="Institution"
                            value={education.institution || ''}
                            onChange={(e) => setEducation({ ...education, institution: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Degree"
                            value={education.degree || ''}
                            onChange={(e) => setEducation({ ...education, degree: e.target.value })}
                        />
                    </div>
                );
            case 4:
                return (
                    <div className="form-step fade-in">
                        <h2>Project</h2>
                        <input
                            type="text"
                            placeholder="Project Name"
                            value={project.name || ''}
                            onChange={(e) => setProject({ ...project, name: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Description"
                            value={project.description || ''}
                            onChange={(e) => setProject({ ...project, description: e.target.value })}
                        />
                    </div>
                );
            case 5:
                return (
                    <div className="form-step fade-in">
                        <h2>Certification</h2>
                        <input
                            type="text"
                            placeholder="Title"
                            value={certification.title || ''}
                            onChange={(e) => setCertification({ ...certification, title: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Achievement"
                            value={certification.achievement || ''}
                            onChange={(e) => setCertification({ ...certification, achievement: e.target.value })}
                        />
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div>
            {renderStepContent()}
            <button onClick={handleNext}>
                {step < 5 ? 'Next' : 'Complete'}
            </button>
        </div>
    );
};

export default MultiStepForm;
