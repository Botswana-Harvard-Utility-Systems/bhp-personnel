from django.utils.translation import gettext_lazy as _
from edc_constants.constants import OTHER

CONTRACT_LENGTH = (
    ('2 Years', '2 Years'),
    ('1 Year', '1 Year'),
    ('6 Months', '6 Months'),
)

CONTRACT_STATUS = (
    ('Active', 'Active'),
    ('Not Active', 'Not Active'),
)

PERFORMANCE_RATING = (
    ('0', 'Not Rated'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

ASSESSMENT_TYPE = (
    ('mid_year', 'Mid Year Assessment'),
    ('year_end', 'Year End Assessment'),
    ('contract_end', 'End of Contract Assessment'))

SALUTATIONS = (
    ('mr', 'Mr'),
    ('ms', 'Ms'),
    ('mrs', 'Mrs'),
    ('dr', 'Dr'),
)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('passport', 'Passport'),
    ('birth_certificate', 'Birth Certificate'),
    (OTHER, _('Other')),
)

HIGHEST_QUALIFICATION = (
    ('None', 'None'),
    ('primary', 'Primary'),
    ('junior_secondary', 'Junior Secondary'),
    ('senior_Secondary', 'Senior Secondary'),
    ('diploma', 'Diploma'),
    ('graduate_certificate', 'Graduate certificate'),
    ('associates_degree', 'Associates degree'),
    ('graduate_diploma', 'Graduate diploma'),
    ('tertiary', 'Tertiary'),
    ('bachelor_degree', 'Bachelor degree'),
    ('masters_degree', 'Masters degree'),
    ('doctoral_degree', 'Doctoral degree'),
    ('phd', 'PhD'),
    ('postdoctoral', 'Postdoctoral')
)
