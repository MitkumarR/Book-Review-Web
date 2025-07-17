# **Book Review Platform**

Welcome to the **Book Review Platform**! 
This project is for book lovers who want to explore, review, and share their thoughts on books. 
It provides features for managing books, genres, user profiles, and reviews.

---

## **Features**

### **For Users**
- **Sign Up & Login**: Create an account to explore the platform.
- **Profile Management**: 
   - Edit your profile details and upload a profile picture.
   - Change password
   - Verify Email
- **Password**: User can reset password through email if they forget it.
- **Book Reviews**: 
  - Leave a review for books you've read (one review per book).
  - Edit or update your existing reviews.
- **Genres**: Explore books by genres, such as Art, Science, and more.
- **Book Search**: Search for books by title.
- **Book Details**: View book details, including author, publication date, and ratings.
- **User Reviews**: 
   - View reviews from other users for a book.
   - User can like other reviews
- **Rating System**: Rate books based on your experience (1-5 stars).

### **For Books**
- **Book Management**: 
  - Add books with multiple genres.
  - Display detailed information about each book, including user reviews.
- **Genres**: Categorize books into multiple genres for better discoverability.

### **For Admins**
- Manage users, books, and genres via the Django Admin Panel.

---
## **Project Setup**

### **Prerequisites**
- Python 3.8+
- Django 4.x
- PostgreSQL( used in this project ) or SQLite (default) or other databases 

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/MitkumarR/Book-Review-Web.git
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations and create a superuser:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## **Database Structure**

- **Books**: Stores book details. Many-to-Many relationship with `Genre`.
- **Genres**: Categorize books.
- **Users**: Stores user details, including profile picture and personal info.
- **Reviews**: A user can leave one review per book but can edit it.

---

## **Contributing**

We welcome contributions! Here's how you can get involved:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push the branch and create a Pull Request.

---

## **Future Enhancements**

- Enable users to follow each other and see their activity.
- Make better UI, using React
- Integrate recommendations based on genres and user preferences.
- Application of Other book's data API like goodread or 
- Add User sign in by Gmail or Apple ID
- Add a feature to save books for later
---

## **Contact**

If you have any questions or suggestions, feel free to reach out at [mitkumar1977@gamil.com].