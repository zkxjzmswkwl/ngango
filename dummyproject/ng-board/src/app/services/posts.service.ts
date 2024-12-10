import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Board } from '../models/posts.struct';


@Injectable({providedIn: 'root'})
export class PostsService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);

  list(): Observable<Board[]> {
    return this.http.get<Board[]>(`${this.url}/posts/`);
  }

  create(data: {}): Observable<Board> {
    return this.http.post<Board>(`${this.url}/posts/`, data);
  }

  retrieve(): Observable<Board[]> {
    return this.http.get<Board[]>(`${this.url}/posts/`);
  }

  update(data: {}): Observable<Board> {
    return this.http.put<Board>(`${this.url}/posts/`, data);
  }

  destroy(): Observable<any> {
    return this.http.delete<Board[]>(`${this.url}/posts/`);
  }
}
