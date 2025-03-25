import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent {
  regulatoryText = '';
  csvFile: File | null = null;
  results: any = null;
  loading = false;
  error = '';

  constructor(private http: HttpClient) {}

  onFileChange(event: any) {
    this.csvFile = event.target.files[0];
  }

  onSubmit() {
    if (!this.csvFile || !this.regulatoryText) {
      this.error = 'Please upload a CSV file and enter regulatory text.';
      return;
    }

    this.loading = true;
    this.error = '';
    
    const formData = new FormData();
    formData.append('csv_file', this.csvFile);
    formData.append('regulatory_text', this.regulatoryText);

    this.http.post('http://localhost:5000/process', formData).subscribe(
      (response: any) => {
        this.results = response;
        this.loading = false;
      },
      (error) => {
        this.error = 'An error occurred while processing your request.';
        this.loading = false;
        console.error('Error:', error);
      }
    );
  }
}
