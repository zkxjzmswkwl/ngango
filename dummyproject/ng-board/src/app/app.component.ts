import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PostsService } from './services/posts.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'ng-board';
  boardName: string = '';
  boardDescription: string = '';
  private postService: PostsService = inject(PostsService);

  ngOnInit(): void {
    this.postService.list().subscribe((data) => {
      console.log(data);
    });
  }

  addBoard(): void {
    this.postService.create({name: this.boardName, description: this.boardDescription}).subscribe((data) => {
      console.log(data);
    })
  }
}
