import React, { useState } from 'react';
import { PersonalInfo, Experience, Education, Project, Certification, Address } from '../types';
import './form.css';

interface MultiStepFormProps {
    onComplete: () => void;
}

const countries = ["United States", "Canada", "United Kingdom", "Australia", "Germany", "France", "India", "China", "Japan", "Mexico"]; // Add more countries as needed

const MultiStepForm: React.FC<MultiStepFormProps> = ({ onComplete }) => {
    const [step, setStep] = useState(0);
    const [personalInfo, setPersonalInfo] = useState<Partial<PersonalInfo>>({});
    const [address, setAddress] = useState<Partial<Address>>({});
    const [experiences, setExperiences] = useState<Experience[]>([{ company: '', position: '', start_date: '', end_date: '', responsibilities: '', details: '' }]);
    const [educations, setEducations] = useState<Education[]>([{ institution: '', degree: '', major: '', start_date: '', end_date: '', minor: '', gpa: undefined, max_gpa: undefined, honours: '', details: '' }]);
    const [projects, setProjects] = useState<Project[]>([{ name: '', description: '', technologies: [], role: '', url: '', start_date: '', end_date: '' }]);
    const [certifications, setCertifications] = useState<Certification[]>([{ title: '', achievement: '', date: '' }]);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});

    const validatePersonalInfo = () => {
        const newErrors: { [key: string]: string } = {};
        if (!personalInfo.first_name) newErrors.first_name = "First Name is required.";
        if (!personalInfo.last_name) newErrors.last_name = "Last Name is required.";
        if (!personalInfo.email) newErrors.email = "Email is required.";
        else if (!/\S+@\S+\.\S+/.test(personalInfo.email)) newErrors.email = "Email is invalid.";
        if (!personalInfo.phone) newErrors.phone = "Phone number is required.";
        else if (!/^\d+$/.test(personalInfo.phone)) newErrors.phone = "Phone number must be numeric.";
        if (!personalInfo.date_of_birth) newErrors.date_of_birth = "Date of Birth is required.";

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const validateAddress = () => {
        const newErrors: { [key: string]: string } = {};
        if (!address.street) newErrors.street = "Street is required.";
        if (!address.city) newErrors.city = "City is required.";
        if (!address.state) newErrors.state = "State is required.";
        if (!address.zip) newErrors.zip = "Zip is required.";
        if (!address.country) newErrors.country = "Country is required.";

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const validateExperiences = () => {
        const newErrors: { [key: string]: string } = {};
        experiences.forEach((experience, index) => {
            if (experience.end_date && !experience.start_date) {
                newErrors[`experience_start_date_${index}`] = "Start date is required if end date is given.";
            }
            if (experience.start_date && experience.end_date && new Date(experience.start_date) > new Date(experience.end_date)) {
                newErrors[`experience_date_${index}`] = "Start date cannot be later than end date.";
            }
        });

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const validateEducations = () => {
        const newErrors: { [key: string]: string } = {};
        educations.forEach((education, index) => {
            if (education.gpa !== undefined && education.max_gpa === undefined) {
                newErrors[`education_max_gpa_${index}`] = "Max GPA is required if GPA is provided.";
            }
            if (education.gpa !== undefined && education.max_gpa !== undefined && education.gpa > education.max_gpa) {
                newErrors[`education_gpa_${index}`] = "GPA cannot exceed the maximum GPA.";
            }
            if (education.end_date && !education.start_date) {
                newErrors[`education_start_date_${index}`] = "Start date is required if end date is given.";
            }
            if (education.start_date && education.end_date && new Date(education.start_date) > new Date(education.end_date)) {
                newErrors[`education_date_${index}`] = "Start date cannot be later than end date.";
            }
        });

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const validateProjects = () => {
        const newErrors: { [key: string]: string } = {};
        projects.forEach((project, index) => {
            if (project.end_date && !project.start_date) {
                newErrors[`project_start_date_${index}`] = "Start date is required if end date is given.";
            }
            if (project.start_date && project.end_date && new Date(project.start_date) > new Date(project.end_date)) {
                newErrors[`project_date_${index}`] = "Start date cannot be later than end date.";
            }
        });

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleNext = () => {
        if (step === 1 && !validatePersonalInfo()) return;
        if (step === 2 && !validateAddress()) return;
        if (step === 3 && !validateExperiences()) return;
        if (step === 4 && !validateEducations()) return;
        if (step === 5 && !validateProjects()) return;

        if (step < 6) {
            setStep(step + 1);
        } else {
            onComplete();
        }
    };

    const handleBack = () => {
        if (step > 0) {
            setStep(step - 1);
        }
    };

    const handleExperienceChange = (index: number, field: keyof Experience, value: any) => {
        const updatedExperiences = [...experiences];
        updatedExperiences[index][field] = value;
        setExperiences(updatedExperiences);
    };

    const addExperience = () => {
        setExperiences([...experiences, { company: '', position: '', start_date: '', end_date: '', responsibilities: '', details: '' }]);
    };

    const deleteExperience = (index: number) => {
        const updatedExperiences = experiences.filter((_, i) => i !== index);
        setExperiences(updatedExperiences);
    };

    const handleEducationChange = (index: number, field: keyof Education, value: any) => {
        const updatedEducations = [...educations];
        if (field === 'gpa' || field === 'max_gpa') {
            updatedEducations[index][field] = parseFloat(value);
        } else {
            updatedEducations[index][field] = value;
        }
        setEducations(updatedEducations);
    };

    const addEducation = () => {
        setEducations([...educations, { institution: '', degree: '', major: '', start_date: '', end_date: '', minor: '', gpa: undefined, max_gpa: undefined, honours: '', details: '' }]);
    };

    const deleteEducation = (index: number) => {
        const updatedEducations = educations.filter((_, i) => i !== index);
        setEducations(updatedEducations);
    };

    const handleProjectChange = (index: number, field: keyof Project, value: any) => {
        const updatedProjects = [...projects];
        if (field === 'technologies') {
            updatedProjects[index][field] = value.split(',').map((tech: string) => tech.trim());
        } else {
            updatedProjects[index][field] = value;
        }
        setProjects(updatedProjects);
    };

    const addProject = () => {
        setProjects([...projects, { name: '', description: '', technologies: [], role: '', url: '', start_date: '', end_date: '' }]);
    };

    const deleteProject = (index: number) => {
        const updatedProjects = projects.filter((_, i) => i !== index);
        setProjects(updatedProjects);
    };

    const handleCertificationChange = (index: number, field: keyof Certification, value: any) => {
        const updatedCertifications = [...certifications];
        updatedCertifications[index][field] = value;
        setCertifications(updatedCertifications);
    };

    const addCertification = () => {
        setCertifications([...certifications, { title: '', achievement: '', date: '' }]);
    };

    const deleteCertification = (index: number) => {
        const updatedCertifications = certifications.filter((_, i) => i !== index);
        setCertifications(updatedCertifications);
    };

    const renderStepContent = () => {
        switch (step) {
            case 0:
                return (
                    <div className="form-step fade-in">
                        <img src="/logo.png" alt="Logo" className="logo" />
                        <h2>Welcome!</h2>
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
                            className={errors.first_name ? "error" : ""}
                        />
                        {errors.first_name && <p className="error-message">{errors.first_name}</p>}
                        <input
                            type="text"
                            placeholder="Last Name"
                            value={personalInfo.last_name || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, last_name: e.target.value })}
                            className={errors.last_name ? "error" : ""}
                        />
                        {errors.last_name && <p className="error-message">{errors.last_name}</p>}
                        <input
                            type="email"
                            placeholder="Email"
                            value={personalInfo.email || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, email: e.target.value })}
                            className={errors.email ? "error" : ""}
                        />
                        {errors.email && <p className="error-message">{errors.email}</p>}
                        <input
                            type="tel"
                            placeholder="Phone"
                            value={personalInfo.phone || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, phone: e.target.value })}
                            className={errors.phone ? "error" : ""}
                        />
                        {errors.phone && <p className="error-message">{errors.phone}</p>}
                        <input
                            type="date"
                            placeholder="Date of Birth"
                            value={personalInfo.date_of_birth || ''}
                            onChange={(e) => setPersonalInfo({ ...personalInfo, date_of_birth: e.target.value })}
                            className={errors.date_of_birth ? "error" : ""}
                        />
                        {errors.date_of_birth && <p className="error-message">{errors.date_of_birth}</p>}
                    </div>
                );
            case 2:
                return (
                    <div className="form-step fade-in">
                        <h2>Address Information</h2>
                        <input
                            type="text"
                            placeholder="Street"
                            value={address.street || ''}
                            onChange={(e) => setAddress({ ...address, street: e.target.value })}
                            className={errors.street ? "error" : ""}
                        />
                        {errors.street && <p className="error-message">{errors.street}</p>}
                        <input
                            type="text"
                            placeholder="City"
                            value={address.city || ''}
                            onChange={(e) => setAddress({ ...address, city: e.target.value })}
                            className={errors.city ? "error" : ""}
                        />
                        {errors.city && <p className="error-message">{errors.city}</p>}
                        <input
                            type="text"
                            placeholder="State"
                            value={address.state || ''}
                            onChange={(e) => setAddress({ ...address, state: e.target.value })}
                            className={errors.state ? "error" : ""}
                        />
                        {errors.state && <p className="error-message">{errors.state}</p>}
                        <input
                            type="text"
                            placeholder="Zip"
                            value={address.zip || ''}
                            onChange={(e) => setAddress({ ...address, zip: e.target.value })}
                            className={errors.zip ? "error" : ""}
                        />
                        {errors.zip && <p className="error-message">{errors.zip}</p>}
                        <select
                            value={address.country || ''}
                            onChange={(e) => setAddress({ ...address, country: e.target.value })}
                            className={`input ${errors.country ? "error" : ""}`}
                        >
                            <option value="">Select Country</option>
                            {countries.map((country, index) => (
                                <option key={index} value={country}>
                                    {country}
                                </option>
                            ))}
                        </select>
                        {errors.country && <p className="error-message">{errors.country}</p>}
                    </div>
                );
            case 3:
                return (
                    <div className="form-step fade-in">
                        <h2>Experience</h2>
                        {experiences.map((experience, index) => (
                            <div key={index} className="experience-entry">
                                {index > 0 && (
                                    <button
                                        type="button"
                                        className="delete-button"
                                        onClick={() => deleteExperience(index)}
                                    >
                                        &times;
                                    </button>
                                )}
                                <input
                                    type="text"
                                    placeholder="Company"
                                    value={experience.company}
                                    onChange={(e) => handleExperienceChange(index, 'company', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Position"
                                    value={experience.position}
                                    onChange={(e) => handleExperienceChange(index, 'position', e.target.value)}
                                />
                                <input
                                    type="date"
                                    placeholder="Start Date"
                                    value={experience.start_date}
                                    onChange={(e) => handleExperienceChange(index, 'start_date', e.target.value)}
                                    className={errors[`experience_start_date_${index}`] ? "error" : ""}
                                />
                                {errors[`experience_start_date_${index}`] && <p className="error-message">{errors[`experience_start_date_${index}`]}</p>}
                                <input
                                    type="date"
                                    placeholder="End Date"
                                    value={experience.end_date || ''}
                                    onChange={(e) => handleExperienceChange(index, 'end_date', e.target.value)}
                                    className={errors[`experience_date_${index}`] ? "error" : ""}
                                />
                                {errors[`experience_date_${index}`] && <p className="error-message">{errors[`experience_date_${index}`]}</p>}
                                <textarea
                                    placeholder="Responsibilities"
                                    value={experience.responsibilities}
                                    onChange={(e) => handleExperienceChange(index, 'responsibilities', e.target.value)}
                                />
                                <textarea
                                    placeholder="Details"
                                    value={experience.details || ''}
                                    onChange={(e) => handleExperienceChange(index, 'details', e.target.value)}
                                />
                            </div>
                        ))}
                        <button className="form-button" type="button" onClick={addExperience}>
                            Add Another Experience
                        </button>
                    </div>
                );
            case 4:
                return (
                    <div className="form-step fade-in">
                        <h2>Education</h2>
                        {educations.map((education, index) => (
                            <div key={index} className="education-entry">
                                {index > 0 && (
                                    <button
                                        type="button"
                                        className="delete-button"
                                        onClick={() => deleteEducation(index)}
                                    >
                                        &times;
                                    </button>
                                )}
                                <input
                                    type="text"
                                    placeholder="Institution"
                                    value={education.institution}
                                    onChange={(e) => handleEducationChange(index, 'institution', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Degree"
                                    value={education.degree}
                                    onChange={(e) => handleEducationChange(index, 'degree', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Major"
                                    value={education.major}
                                    onChange={(e) => handleEducationChange(index, 'major', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Minor"
                                    value={education.minor || ''}
                                    onChange={(e) => handleEducationChange(index, 'minor', e.target.value)}
                                />
                                <input
                                    type="number"
                                    placeholder="GPA"
                                    value={education.gpa || ''}
                                    onChange={(e) => handleEducationChange(index, 'gpa', parseFloat(e.target.value))}
                                    className={errors[`education_gpa_${index}`] ? "error" : ""}
                                />
                                {errors[`education_gpa_${index}`] && <p className="error-message">{errors[`education_gpa_${index}`]}</p>}
                                <input
                                    type="number"
                                    placeholder="Max GPA"
                                    value={education.max_gpa || ''}
                                    onChange={(e) => handleEducationChange(index, 'max_gpa', parseFloat(e.target.value))}
                                    className={errors[`education_max_gpa_${index}`] ? "error" : ""}
                                />
                                {errors[`education_max_gpa_${index}`] && <p className="error-message">{errors[`education_max_gpa_${index}`]}</p>}
                                <input
                                    type="text"
                                    placeholder="Honours"
                                    value={education.honours || ''}
                                    onChange={(e) => handleEducationChange(index, 'honours', e.target.value)}
                                />
                                <input
                                    type="date"
                                    placeholder="Start Date"
                                    value={education.start_date}
                                    onChange={(e) => handleEducationChange(index, 'start_date', e.target.value)}
                                    className={errors[`education_start_date_${index}`] ? "error" : ""}
                                />
                                {errors[`education_start_date_${index}`] && <p className="error-message">{errors[`education_start_date_${index}`]}</p>}
                                <input
                                    type="date"
                                    placeholder="End Date"
                                    value={education.end_date || ''}
                                    onChange={(e) => handleEducationChange(index, 'end_date', e.target.value)}
                                    className={errors[`education_date_${index}`] ? "error" : ""}
                                />
                                {errors[`education_date_${index}`] && <p className="error-message">{errors[`education_date_${index}`]}</p>}
                                <textarea
                                    placeholder="Details"
                                    value={education.details || ''}
                                    onChange={(e) => handleEducationChange(index, 'details', e.target.value)}
                                />
                            </div>
                        ))}
                        <button className="form-button" type="button" onClick={addEducation}>
                            Add Another Education
                        </button>
                    </div>
                );
            case 5:
                return (
                    <div className="form-step fade-in">
                        <h2>Project</h2>
                        {projects.map((project, index) => (
                            <div key={index} className="project-entry">
                                {index > 0 && (
                                    <button
                                        type="button"
                                        className="delete-button"
                                        onClick={() => deleteProject(index)}
                                    >
                                        &times;
                                    </button>
                                )}
                                <input
                                    type="text"
                                    placeholder="Project Name"
                                    value={project.name}
                                    onChange={(e) => handleProjectChange(index, 'name', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Description"
                                    value={project.description}
                                    onChange={(e) => handleProjectChange(index, 'description', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Technologies (comma-separated)"
                                    value={project.technologies.join(', ')}
                                    onChange={(e) => handleProjectChange(index, 'technologies', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Role"
                                    value={project.role}
                                    onChange={(e) => handleProjectChange(index, 'role', e.target.value)}
                                />
                                <input
                                    type="url"
                                    placeholder="URL"
                                    value={project.url || ''}
                                    onChange={(e) => handleProjectChange(index, 'url', e.target.value)}
                                />
                                <input
                                    type="date"
                                    placeholder="Start Date"
                                    value={project.start_date}
                                    onChange={(e) => handleProjectChange(index, 'start_date', e.target.value)}
                                    className={errors[`project_start_date_${index}`] ? "error" : ""}
                                />
                                {errors[`project_start_date_${index}`] && <p className="error-message">{errors[`project_start_date_${index}`]}</p>}
                                <input
                                    type="date"
                                    placeholder="End Date"
                                    value={project.end_date || ''}
                                    onChange={(e) => handleProjectChange(index, 'end_date', e.target.value)}
                                    className={errors[`project_date_${index}`] ? "error" : ""}
                                />
                                {errors[`project_date_${index}`] && <p className="error-message">{errors[`project_date_${index}`]}</p>}
                            </div>
                        ))}
                        <button className="form-button" type="button" onClick={addProject}>
                            Add Another Project
                        </button>
                    </div>
                );
            case 6:
                return (
                    <div className="form-step fade-in">
                        <h2>Certification</h2>
                        {certifications.map((certification, index) => (
                            <div key={index} className="certification-entry">
                                {index > 0 && (
                                    <button
                                        type="button"
                                        className="delete-button"
                                        onClick={() => deleteCertification(index)}
                                    >
                                        &times;
                                    </button>
                                )}
                                <input
                                    type="text"
                                    placeholder="Title"
                                    value={certification.title}
                                    onChange={(e) => handleCertificationChange(index, 'title', e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Achievement"
                                    value={certification.achievement}
                                    onChange={(e) => handleCertificationChange(index, 'achievement', e.target.value)}
                                />
                                <input
                                    type="date"
                                    placeholder="Date"
                                    value={certification.date}
                                    onChange={(e) => handleCertificationChange(index, 'date', e.target.value)}
                                />
                            </div>
                        ))}
                        <button className="form-button" type="button" onClick={addCertification}>
                            Add Another Certification
                        </button>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div>
            {renderStepContent()}
            <div className={`button-container ${step === 0 ? 'center' : ''}`}>
                {step > 0 && <button className="form-button" onClick={handleBack}>Back</button>}
                <button className="form-button" onClick={handleNext}>
                    {step < 6 ? 'Next' : 'Complete'}
                </button>
            </div>
        </div>
    );
};

export default MultiStepForm;
