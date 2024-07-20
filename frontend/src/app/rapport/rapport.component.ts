import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import jsPDF from 'jspdf';

@Component({
  selector: 'app-rapport',
  templateUrl: './rapport.component.html',
  styleUrls: ['./rapport.component.css']
})
export class RapportComponent implements OnInit {
  reportData: any;

  constructor(private router: Router) {
    const navigation = this.router.getCurrentNavigation();
    if (navigation && navigation.extras.state && navigation.extras.state['result']) {
      this.reportData = navigation.extras.state['result'];
    } else {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {}

  formatReportData(data: string): string {
    if (typeof data === 'string') {
      // Remplacer les sauts de ligne par des <br>
      return data.replace(/\n/g, '<br/>');
    } else {
      // Convertir en JSON string si ce n'est pas une chaîne
      return JSON.stringify(data, null, 2).replace(/\n/g, '<br/>');
    }
  }

  generatePDF() {
    const doc = new jsPDF();
    const marginLeft = 10;
    const marginTop = 10;
    const lineHeight = 10;
    const pageHeight = doc.internal.pageSize.height;
    const pageWidth = doc.internal.pageSize.width;
    const maxWidth = pageWidth - marginLeft * 2;
    const title = 'Résultats du rapport';

    
    
    let content = typeof this.reportData === 'string' ? this.reportData : JSON.stringify(this.reportData, null, 2);
    const lines = doc.splitTextToSize(content, maxWidth);
  
    doc.setFontSize(14);
    doc.text(title, marginLeft, marginTop);
  
    let y = marginTop + lineHeight; // Position Y de départ après le titre
  
    lines.forEach((line: any) => {
      if (y + lineHeight > pageHeight) {
        doc.addPage();
        y = marginTop; // Reset y position for new page
      }
      doc.text(line, marginLeft, y);
      y += lineHeight; // Avance de 10 unités pour chaque ligne
    });
  
    doc.save('rapport.pdf');
  }
  
  
}
