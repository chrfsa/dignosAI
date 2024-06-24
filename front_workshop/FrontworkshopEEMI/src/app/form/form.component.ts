import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../service/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent {
  myForm: FormGroup;
  errorMessage: string | undefined;
  showAlert: boolean = false;

  constructor(private fb: FormBuilder, private apiService: ApiService, private router: Router) {
    this.myForm = this.fb.group({
      nom: ['', Validators.required],
      age: ['', [Validators.required, Validators.min(0)]], // Âge doit être un nombre positif
      poids: ['', [Validators.required, Validators.min(0)]], // Poids doit être un nombre positif
      symptoms: ['', Validators.required],
      patient_history: ['non'],
    });
  }

  get nom() { return this.myForm.get('nom'); }
  get age() { return this.myForm.get('age'); }
  get poids() { return this.myForm.get('poids'); }
  get symptoms() { return this.myForm.get('symptoms'); }
  get patient_history() { return this.myForm.get('patient_history'); }

  onSubmit() {
    if (this.myForm.valid) {
      this.showAlert = false;
      const formData = this.myForm.value;
      this.apiService.runMedicalCrew(formData).subscribe(
        (response) => {
          if (response.status === 'success') {
            this.router.navigate(['/report'], { state: { result: response.result } });
          } else {
            this.errorMessage = 'Erreur lors de l\'exécution de la requête.';
            this.showAlert = true;
          }
        },
        (error) => {
          this.errorMessage = 'Erreur lors de l\'exécution de la requête.';
          this.showAlert = true;
        }
      );
    } else {
      this.errorMessage = 'Veuillez remplir tous les champs requis.';
      this.showAlert = true;
    }
  }
}
