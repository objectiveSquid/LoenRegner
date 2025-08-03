from config import MINIMUM_PASSWORD_CHARACTERS

INVALID_SESSION_TEXT = "Ugyldig session, prøv at logge ud og ind igen."
INVALID_DATE_TEXT = "Ugyldig datoformat, skal være som dd/mm/åååå"
INVALID_TIME_TEXT = "Ugyldig tidsformat, skal være som 12:00"
MISSING_PARAMETERS_TEXT = "Mangelende parametre"
HOURLY_MUST_BE_POSITIVE_NUMBER_TEXT = "Timeløn skal være et positivt tal"
STOP_TIME_MUST_BE_AFTER_START_TIME_TEXT = (
    "Stop tidspunkt skal være efter start tidspunkt"
)
INVALID_CREDENTIALS_TEXT = "Ugyldige login oplysninger"
INVALID_PASSWORD_TEXT = f"Adgangskode skal være over {MINIMUM_PASSWORD_CHARACTERS} tegn"
USERNAME_TAKEN_TEXT = "Brugernavnet er allerede i brug"
INVALID_OLD_PASSWORD_TEXT = "Nuværende adgangskode er forkert"
TAX_START_MUST_BE_POSITIVE_NUMBER_TEXT = (
    "Hvornår skat begynder skal være et positivt tal (eller 0)"
)

SUCCESS_TEXT = "Success"
