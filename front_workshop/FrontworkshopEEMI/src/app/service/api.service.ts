// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Interface pour représenter la structure de la réponse API
export interface ApiResponse {
  status: string;
  result: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/run_medical_crew'; // Remplacez par l'URL de votre API Flask

  constructor(private http: HttpClient) { }

  // Spécifier le type de réponse attendu dans la fonction
  runMedicalCrew(data: any): Observable<ApiResponse> {
    return this.http.post<ApiResponse>(this.apiUrl, data);
  }
}
