from enum import Enum
import re
import streamlit as st

class ConversationStage(Enum):
    GREETING = "greeting"
    COLLECT_NAME = "collect_name"
    COLLECT_EMAIL = "collect_email"
    COLLECT_PHONE = "collect_phone"
    COLLECT_EXPERIENCE = "collect_experience"
    COLLECT_POSITION = "collect_position"
    COLLECT_LOCATION = "collect_location"
    COLLECT_TECH_STACK = "collect_tech_stack"
    TECHNICAL_QUESTIONS = "technical_questions"
    FAREWELL = "farewell"

class HiringBot:
    def __init__(self):
        self.candidate_info = {}
        self.technical_questions_asked = False
        self.languages = {
            'en': self.get_english_responses(),
            'es': self.get_spanish_responses(),
            'fr': self.get_french_responses()
        }
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        pattern = r'^\+?1?\d{9,15}$'
        return re.match(pattern, phone) is not None

    def get_english_responses(self):
        return {
            'greeting': "Hello! I'm the TalentScout Hiring Assistant. I'll help evaluate your technical profile. Could you please tell me your full name?",
            'ask_email': "Nice to meet you, {}! Could you please share your email address?",
            'ask_phone': "Thanks! Now, could you please provide your phone number?",
            'ask_experience': "How many years of experience do you have in the tech industry?",
            'ask_position': "What position are you interested in applying for?",
            'ask_location': "What is your current location?",
            'ask_tech_stack': "Please list your tech stack (programming languages, frameworks, and tools you're proficient in, separated by commas):",
            'invalid_email': "That doesn't look like a valid email address. Please try again.",
            'invalid_phone': "That doesn't look like a valid phone number. Please enter a valid phone number.",
            'invalid_experience': "Please enter a valid number for your years of experience.",
            'session_ended': "The interview session has ended. If you'd like to start a new session, please refresh the page."
        }

    def get_spanish_responses(self):
        return {
            'greeting': "¡Hola! Soy el Asistente de Contratación de TalentScout. Te ayudaré a evaluar tu perfil técnico. ¿Podrías decirme tu nombre completo?",
            'ask_email': "¡Encantado de conocerte, {}! ¿Podrías compartir tu dirección de correo electrónico?",
            'ask_phone': "¡Gracias! Ahora, ¿podrías proporcionar tu número de teléfono?",
            'ask_experience': "¿Cuántos años de experiencia tienes en la industria tecnológica?",
            'ask_position': "¿Qué posición te interesa solicitar?",
            'ask_location': "¿Cuál es tu ubicación actual?",
            'ask_tech_stack': "Por favor, enumera tu stack tecnológico (lenguajes de programación, frameworks y herramientas en las que eres competente, separados por comas):",
            'invalid_email': "Eso no parece una dirección de correo electrónico válida. Por favor, inténtalo de nuevo.",
            'invalid_phone': "Eso no parece un número de teléfono válido. Por favor, ingresa un número válido.",
            'invalid_experience': "Por favor, ingresa un número válido para tus años de experiencia.",
            'session_ended': "La sesión de entrevista ha terminado. Si deseas iniciar una nueva sesión, actualiza la página."
        }

    def get_french_responses(self):
        return {
            'greeting': "Bonjour! Je suis l'Assistant de Recrutement TalentScout. Je vais vous aider à évaluer votre profil technique. Pourriez-vous me dire votre nom complet?",
            'ask_email': "Ravi de vous rencontrer, {}! Pourriez-vous partager votre adresse email?",
            'ask_phone': "Merci! Maintenant, pourriez-vous fournir votre numéro de téléphone?",
            'ask_experience': "Combien d'années d'expérience avez-vous dans l'industrie technologique?",
            'ask_position': "Quel poste vous intéresse?",
            'ask_location': "Quelle est votre localisation actuelle?",
            'ask_tech_stack': "Veuillez lister votre stack technique (langages de programmation, frameworks et outils que vous maîtrisez, séparés par des virgules):",
            'invalid_email': "Cela ne ressemble pas à une adresse email valide. Veuillez réessayer.",
            'invalid_phone': "Cela ne ressemble pas à un numéro de téléphone valide. Veuillez entrer un numéro valide.",
            'invalid_experience': "Veuillez entrer un nombre valide pour vos années d'expérience.",
            'session_ended': "La session d'entretien est terminée. Si vous souhaitez démarrer une nouvelle session, veuillez actualiser la page."
        }

    def get_response(self, message, current_stage):
        """Generate response based on current conversation stage"""
        lang = getattr(st.session_state, 'language', 'en')
        responses = self.languages[lang]

        if current_stage == ConversationStage.GREETING.value:
            return {
                "response": responses['greeting'],
                "next_stage": ConversationStage.COLLECT_NAME.value
            }
        
        elif current_stage == ConversationStage.COLLECT_NAME.value:
            self.candidate_info['name'] = message
            return {
                "response": responses['ask_email'].format(message),
                "next_stage": ConversationStage.COLLECT_EMAIL.value
            }
            
        elif current_stage == ConversationStage.COLLECT_EMAIL.value:
            if self.validate_email(message):
                self.candidate_info['email'] = message
                return {
                    "response": responses['ask_phone'],
                    "next_stage": ConversationStage.COLLECT_PHONE.value
                }
            else:
                return {
                    "response": responses['invalid_email'],
                    "next_stage": current_stage
                }

        elif current_stage == ConversationStage.COLLECT_PHONE.value:
            if self.validate_phone(message):
                self.candidate_info['phone'] = message
                return {
                    "response": responses['ask_experience'],
                    "next_stage": ConversationStage.COLLECT_EXPERIENCE.value
                }
            else:
                return {
                    "response": responses['invalid_phone'],
                    "next_stage": current_stage
                }

        elif current_stage == ConversationStage.COLLECT_EXPERIENCE.value:
            try:
                experience = float(message)
                self.candidate_info['experience'] = experience
                return {
                    "response": responses['ask_position'],
                    "next_stage": ConversationStage.COLLECT_POSITION.value
                }
            except ValueError:
                return {
                    "response": responses['invalid_experience'],
                    "next_stage": current_stage
                }

        elif current_stage == ConversationStage.COLLECT_POSITION.value:
            self.candidate_info['position'] = message
            return {
                "response": responses['ask_location'],
                "next_stage": ConversationStage.COLLECT_LOCATION.value
            }

        elif current_stage == ConversationStage.COLLECT_LOCATION.value:
            self.candidate_info['location'] = message
            return {
                "response": responses['ask_tech_stack'],
                "next_stage": ConversationStage.COLLECT_TECH_STACK.value
            }

        elif current_stage == ConversationStage.COLLECT_TECH_STACK.value:
            self.candidate_info['tech_stack'] = [tech.strip() for tech in message.split(',')]
            questions = self.generate_technical_questions()
            self.technical_questions_asked = True
            return {
                "response": questions,
                "next_stage": ConversationStage.TECHNICAL_QUESTIONS.value
            }

        elif current_stage == ConversationStage.TECHNICAL_QUESTIONS.value:
            self.candidate_info['technical_answers'] = message
            return {
                "response": self.generate_farewell(),
                "next_stage": ConversationStage.FAREWELL.value
            }

        elif current_stage == ConversationStage.FAREWELL.value:
            return {
                "response": responses['session_ended'],
                "next_stage": ConversationStage.FAREWELL.value
            }

    def generate_technical_questions(self):
        """Generate technical questions based on the candidate's tech stack"""
        # Previous implementation remains the same
        tech_stack = self.candidate_info.get('tech_stack', [])
        
        tech_questions = {
            'python': [
                "Explain the difference between lists and tuples in Python.",
                "How does memory management work in Python?",
                "What are decorators and how do you use them?"
            ],
            'javascript': [
                "Explain closure in JavaScript.",
                "What's the difference between == and === in JavaScript?",
                "How does prototypal inheritance work?"
            ],
            'java': [
                "Explain the difference between abstract classes and interfaces.",
                "How does garbage collection work in Java?",
                "What are the differences between checked and unchecked exceptions?"
            ],
            'react': [
                "What are React hooks?",
                "Explain the virtual DOM in React.",
                "How does state management work in React?"
            ],
            'sql': [
                "What's the difference between INNER and LEFT JOIN?",
                "Explain indexing in databases.",
                "How do you optimize SQL queries?"
            ],
            'docker': [
                "What is Docker and how does it work?",
                "Explain Docker containers vs VMs.",
                "What are Docker volumes used for?"
            ]
        }
        
        response = "Based on your tech stack, please answer these technical questions:\n\n"
        questions_asked = 0
        
        for tech in tech_stack:
            tech_lower = tech.lower()
            if tech_lower in tech_questions:
                response += f"\nFor {tech}:\n"
                for question in tech_questions[tech_lower][:2]:
                    questions_asked += 1
                    response += f"{questions_asked}. {question}\n"
                if questions_asked >= 5:
                    break
        
        if questions_asked == 0:
            response += "I don't have specific questions for your tech stack, but please describe your experience with these technologies:\n"
            for tech in tech_stack[:3]:
                response += f"- What is your experience with {tech}?\n"
        
        response += "\nPlease provide your answers in a clear and concise manner."
        return response

    def generate_farewell(self):
        """Generate farewell message with next steps"""
        name = self.candidate_info.get('name', 'candidate')
        return f"""Thank you {name} for completing the initial technical screening! 

Here's what happens next:
1. Our team will review your responses
2. If your profile matches our requirements, you'll receive an email within 2-3 business days
3. The email will contain details about the next steps in the interview process

We appreciate your time and interest in joining our team!

Feel free to start a new session if you need to modify any of your responses."""