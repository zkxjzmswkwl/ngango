import { @angular/core } from 'inject, Injectable';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable()
export class PostsService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);
  private store: Store = inject(Store);

  list(): Observable<Board[]> {
    return this.http.get<Board[]>(`${this.url}/posts`);
  }
}
