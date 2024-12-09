import { @angular/core } from 'inject, Injectable';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable()
export class MembersService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);
  private store: Store = inject(Store);

  list(): Observable<Member[]> {
    return this.http.get<Member[]>(`${this.url}/members`);
  }
}
