import { @angular/core } from 'inject, Injectable';
import { @angular/common/http } from 'HttpClient';
import { rxjs } from 'Observable';


@Injectable()
export class MembersService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);
  private store: Store = inject(Store);

  list(): Observable<Member[]> {
    return this.http.get<Member[]>(`${{this.url}}/{self.app.name.lower()}`);
  }

  create(): Observable<Member[]> {
    return this.http.post<Member[]>(`${{this.url}}/{self.app.name.lower()}`);
  }

  retrieve(): Observable<Member[]> {
    return this.http.get<Member[]>(`${{this.url}}/{self.app.name.lower()}`);
  }

  update(): Observable<Member[]> {
    return this.http.put<Member[]>(`${{this.url}}/{self.app.name.lower()}`);
  }

  destroy(): Observable<any> {
    return this.http.delete<Member[]>(`${{this.url}}/{self.app.name.lower()}`);
  }
}
