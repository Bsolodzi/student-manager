 <!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Name -->
<div align="center">
  <h1>The Student Management API</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/bsolodzi/student-manager-api#readme"><strong>Explore the Docs »</strong></a>
    <br />
    <a href="https://github.com/bsolodzi/student-manager-api/blob/main/images/StudentManagerAPI_Full_Page.png">View Demo</a>
    ·
    <a href="https://github.com/bsolodzi/student-manager-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/bsolodzi/student-manager-api/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-The-Student-Management-API">About The Student Management API</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#skills-gained">Skills Gained</a></li>
    <li><a href="#usage">How To Use This API</a></li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact Me</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Project -->
## About The Student Management API

This student management api is a REST API which enables school staff to register accounts and manage student data on the PythonAnywhere-powered web app. CRUD operations can be carried out on the student data, with an easy-to-use Swagger UI setup for testing and integration with the front end.

Students have limited access to the app, as a student can only change their profile details and view their profile, courses, grades and CGPA.

This student management API was built with Python's Flask-RESTX by <a href="https://www.github.com/bsolodzi">Bernard Kwame Solodzi</a> as the third semester exam project for a Diploma in Backend Engineering from <a href="https://altschoolafrica.com/schools/engineering">AltSchool Africa</a>.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Skills Gained

Biulding this API has helped me gain the following skills:
* API Development with Python
* Routing
* Database Management
* User Authentication
* User Authorization
* Testing with pytest and Insomnia
* Debugging
* Web applications Security
* Documentation
* Application Deployment with PythonAnywhere

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Implementation

To use this API, follow these steps:

1. Open the PythonAnywhere web app on your browser: https://bsolodzi.pythonanywhere.com

2. Create an admin or student account:
    - Click 'admin' to reveal a dropdown menu of administration routes, then register an admin account via the '/admin/register' route
    - Click 'students' to reveal a dropdown menu of student routes, then register a student account via the '/students/register' route

3. Sign in via the '/auth/login' route to generate a JWT token. Copy this access token without the quotation marks

4. Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, for example:
   ```
   Bearer this1is2a3rather4long5hex6string
   ```

5. Click 'Authorize' and then 'Close'

6. Now authorized, you can create, view, update and delete students, courses, grades and admins via the many routes in 'students', 'courses' and 'admin'. You can also get:
    - All students taking a course
    - All courses taken by a student
    - A student's grades in percentage (eg: 84.8%) and letters (eg: A)
    - A student's CGPA, calculated based on all grades from all courses they are taking

7. When you're done, click 'Authorize' at top right again to then 'Logout'

**Note:** When using this API in production, please [fork this repo](https://github.com/bsolodzi/student-manager-apil) and uncomment the `@admin_required()` decorator in the create admin route of [the admin views file](https://github.com/bsolodzi/student-manager-api/blob/main/api/admin/views.py). This will ensure that students and other users will not be authorized to access the admin creation route after the first admin is registered.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/bsolodzi/student-manager-api/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact Me-->
## Contact Me

Bernard Kwame Solodzi
| [LinkedIn](https://www.linkedin.com/in/bernard-kwame-solodzi) |
| [Twitter](https://twitter.com/boss_assignment) |
| Email me: bsolodzi@gmail.com |

Project Link: [Student Management API](https://github.com/bsolodzi/student-manager-api)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's Flask Lessons](https://github.com/CalebEmelike)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/bsolodzi/student-manager-api.svg?style=for-the-badge
[contributors-url]: https://github.com/bsolodzi/student-manager-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/bsolodzi/student-manager-api.svg?style=for-the-badge
[forks-url]: https://github.com/bsolodzi/student-manager-api/network/members
[stars-shield]: https://img.shields.io/github/stars/bsolodzi/student-manager-api.svg?style=for-the-badge
[stars-url]: https://github.com/bsolodzi/student-manager-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/bsolodzi/student-manager-api.svg?style=for-the-badge
[issues-url]: https://github.com/bsolodzi/student-manager-api/issues
[license-shield]: https://img.shields.io/github/license/bsolodzi/student-manager-api.svg?style=for-the-badge
[license-url]: https://github.com/bsolodzi/student-manager-api/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@boss_assignment-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/boss_assignment
[twitter-url]: https://twitter.com/boss_assignment
[ze-school-screenshot]: https://github.com/bsolodzi/student-manager-api/blob/main/images/Ze_School_Full_Page.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
