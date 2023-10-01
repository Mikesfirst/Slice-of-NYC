# NYCslice Django Project
 NYCslice is a web application that generates a day in NYC based on user preferences and Yelp's API


## Project Structure

- **static**: Contains images and CSS files used in the project.
- **templates**: Contains HTML files for different pages of the website.
- **slice**: Contains `models.py` and `views.py` files, essential for the backend.
- **NYCslice**: Contains `settings.py` and `urls.py` files, crucial for configuring and routing.

## How to Run

To run the NYCslice Django project, follow these steps:

1. Install Django by running the following command:

   ```bash
   pip install Django

2. Navigate to the project directory:

   ```bash
   cd path/to/NYCslice_project
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the NYCslice website.

## Notes

- The project structure follows a typical Django setup with static files, templates, and app-specific files.
- Ensure you have Python and pip installed before running the project.
