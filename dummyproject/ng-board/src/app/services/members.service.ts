import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({providedIn: 'root'})
export class MembersService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);

  list(): Observable<Member[]> {
    return this.http.get<Member[]>(`${this.url}/members/`);
  }

  create(data: {}): Observable<Member> {
    return this.http.post<Member>(`${this.url}/members/`, data);
  }

  update(data: {}): Observable<Member> {
    return this.http.put<Member>(`${this.url}/members/`, data);
  }

  destroy(): Observable<any> {
    return this.http.delete<Member[]>(`${this.url}/members/`);
  }
}
