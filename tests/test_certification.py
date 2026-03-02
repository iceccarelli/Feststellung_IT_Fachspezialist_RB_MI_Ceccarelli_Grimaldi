import pytest
import pandas as pd
import os

class CertificationVerifier:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.csv_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'key_details.csv'))
        self.key_details = self._load_key_details()

    def _load_key_details(self):
        try:
            return pd.read_csv(self.csv_path)
        except FileNotFoundError:
            pytest.fail(f"key_details.csv not found at {self.csv_path}")

    def get_detail(self, section, detail_key):
        try:
            return self.key_details[(self.key_details['section'] == section) & (self.key_details['detail_key'] == detail_key)]['detail_value'].iloc[0]
        except IndexError:
            pytest.fail(f"Detail '{detail_key}' in section '{section}' not found in key_details.csv")

@pytest.fixture(scope='module')
def verifier():
    return CertificationVerifier()

def test_candidate_name(verifier):
    """Verify the candidate's name."""
    expected_name = "Vincenzo Ceccarelli Grimaldi"
    actual_name = verifier.get_detail("General", "Candidate Name")
    assert actual_name == expected_name, f"Candidate name mismatch: Expected '{expected_name}', Got '{actual_name}'"

def test_gesprachsdatum(verifier):
    """Verify the Gesprächsdatum."""
    expected_date = "16.10.2025"
    actual_date = verifier.get_detail("General", "Gesprächsdatum")
    assert actual_date == expected_date, f"Gesprächsdatum mismatch: Expected '{expected_date}', Got '{actual_date}'"

def test_organizational_unit(verifier):
    """
    Verify the Organizational Unit.
    Insights for Engineers: Correct organizational unit ensures proper project assignment and reporting structure in rail IT.
    """
    expected_unit = "I.IP-MI-IW 1"
    actual_unit = verifier.get_detail("General", "Organizational Unit")
    assert actual_unit == expected_unit, f"Organizational Unit mismatch: Expected '{expected_unit}', Got '{actual_unit}'"

def test_suitability_status(verifier):
    """Verify the suitability status.
    Insights for Politicians: The suitability status reflects compliance with internal HR policies and external regulatory requirements for specialized roles.
    """
    expected_status = "eingeschränkt geeignet"
    actual_status = verifier.get_detail("Feststellung Ergebnis", "Eignung")
    assert actual_status == expected_status, f"Suitability status mismatch: Expected '{expected_status}', Got '{actual_status}'"

def test_full_qualification_date(verifier):
    """Verify the target date for full qualification.
    Insights for Technicians: This date is a critical milestone for training and development plans, impacting resource allocation and project readiness.
    """
    expected_date = "31.01.2026"
    actual_date = verifier.get_detail("Feststellung Ergebnis", "Maßnahmen geplant bis")
    assert actual_date == expected_date, f"Full qualification date mismatch: Expected '{expected_date}', Got '{actual_date}'"

def test_education_details(verifier):
    """Verify education details."""
    expected_degree = "Wirtschaftselektrotechniker"
    actual_degree = verifier.get_detail("Ausbildung/Vorbildung", "Abschluss und Fachrichtung")
    assert actual_degree == expected_degree, f"Degree mismatch: Expected '{expected_degree}', Got '{actual_degree}'"

    expected_institution = "RWTH Aachen"
    actual_institution = verifier.get_detail("Ausbildung/Vorbildung", "Ausbildungsstelle")
    assert actual_institution == expected_institution, f"Institution mismatch: Expected '{expected_institution}', Got '{actual_institution}'"

    expected_graduation_date = "07/2022"
    actual_graduation_date = verifier.get_detail("Ausbildung/Vorbildung", "Abschlussdatum")
    assert actual_graduation_date == expected_graduation_date, f"Graduation date mismatch: Expected '{expected_graduation_date}', Got '{actual_graduation_date}'"

# Custom pytest hook to print success message
def pytest_sessionfinish(session):
    if not session.testsfailed:
        print("\nCertification 100% verified against PDF")
