import { @angular/core } from 'inject, Injectable';
import { @angular/common/http } from 'HttpClient';
import { rxjs } from 'Observable';


@Injectable()
export class PostsService {
  private url: string = 'http://localhost:8000/api';
  private http: HttpClient = inject(HttpClient);
  private store: Store = inject(Store);

}
