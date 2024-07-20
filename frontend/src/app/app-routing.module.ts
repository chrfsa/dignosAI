import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NavbarComponent } from './navbar/navbar.component';
import { FormComponent } from './form/form.component';
import { RapportComponent } from './rapport/rapport.component';

const routes: Routes = [
  {path: "", component:FormComponent},
  {path: "report", component:RapportComponent},



];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
