import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent }  from './app.component';

import { NavbarComponent } from './components/navbar/navbar.component';

import { AboutComponent } from './components/pages/about.component';
import { HomeComponent } from './components/pages/home.component';

import {routing} from './app.routing'

@NgModule({
  imports:      [ BrowserModule, routing ],
  declarations: [ 
                  AppComponent,

                  NavbarComponent,
                  AboutComponent,
                  HomeComponent,
                ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
