from django import forms


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Select a CSV file')

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        # Check if the file extension is valid
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('Invalid file extension. Only CSV files are allowed.')
        return csv_file
