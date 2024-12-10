export interface Board {
  name: string;
  description: string;
  created_at: string;
}
export interface Post {
  owner: number;
  board: number;
  body: string;
  created_at: string;
}
