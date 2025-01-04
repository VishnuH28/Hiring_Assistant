class LanguageHandler:
    def __init__(self):
        self.translations = {
            'en': self.get_english_translations(),
            'es': self.get_spanish_translations(),
            'fr': self.get_french_translations()
        }
        self.current_language = 'en'

    def get_english_translations(self):
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
            'farewell': """Thank you {} for completing the initial technical screening! 

Here's what happens next:
1. Our team will review your responses
2. If your profile matches our requirements, you'll receive an email within 2-3 business days
3. The email will contain details about the next steps in the interview process

We appreciate your time and interest in joining our team!"""
        }

    def get_spanish_translations(self):
        return {
            'greeting': "¡Hola! Soy el Asistente de Contratación de TalentScout. Te ayudaré a evaluar tu perfil técnico. ¿Podrías decirme tu nombre completo?",
            # Add other Spanish translations
        }

    def get_french_translations(self):
        return {
            'greeting': "Bonjour! Je suis l'Assistant de Recrutement TalentScout. Je vais vous aider à évaluer votre profil technique. Pourriez-vous me dire votre nom complet?",
            # Add other French translations
        }

    def get_text(self, key, *args):
        text = self.translations[self.current_language].get(key, self.translations['en'][key])
        if args:
            return text.format(*args)
        return text

    def set_language(self, language_code):
        if language_code in self.translations:
            self.current_language = language_code