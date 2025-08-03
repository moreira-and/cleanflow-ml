# 📚 Reference: Clean Architecture Essencial - ASP .NET Core with C#

This project draws inspiration from the course **Clean Architecture Essencial - ASP .NET Core com C#**, created by José Carlos Macoratti and available on [Udemy](https://www.udemy.com/share/104rq23@ey1gRn0GjZIDdlshztnuOUYJjECngvSIwoCbiQU5nH3vm60gcKuJQB0af-6ARxTuvQ==/).

## 🧠 Course Overview

The course teaches how to build robust, scalable, and maintainable applications using ASP.NET Core and C#, following the principles of **Clean Architecture**. Key topics include:

- Separation of concerns across layers: Domain, Infrastructure, Application, and WebUI
- Principles like **DRY**, **YAGNI**, and **KISS**
- Domain-Driven Design (DDD) fundamentals
- Implementation of design patterns such as **MVC**, **Repository**, and **CQRS**
- Dependency Injection and Inversion of Control
- Security implementation using custom Identity
- Use of Entity Framework Core with Migrations

## 🐍 Python Adaptation

Although the original course is based on C# and .NET Core, the architectural principles are language-agnostic and have been thoughtfully adapted to Python in this project. Here's how:

- **Layered Architecture**: The project is structured into distinct layers (Domain, Infrastructure, Application, Interface) to promote modularity and testability.
- **Dependency Injection**: Implemented using Python techniques and libraries such as `injector` or manual DI patterns.
- **Repository Pattern**: Abstracts data access logic to ensure separation from business rules.
- **CQRS Principles**: Commands and queries are handled separately to improve scalability and clarity.
- **Domain-Driven Design**: Entities and value objects are modeled to reflect the business domain.
- **Testing**: Each layer is independently testable, following the separation of concerns.

## 🎯 Why This Matters

Clean Architecture helps ensure that your application:

- Is easy to maintain and extend
- Has clear boundaries between responsibilities
- Can evolve without major rewrites
- Is testable and scalable

## 📌 Credits

- Course: [Clean Architecture Essencial - ASP .NET Core com C#](https://www.udemy.com/share/104rq23@ey1gRn0GjZIDdlshztnuOUYJjECngvSIwoCbiQU5nH3vm60gcKuJQB0af-6ARxTuvQ==/)
- Instructor: José Carlos Macoratti
- Platform: Udemy

## 🔗 Related Resources

- [Clean Architecture by Robert C. Martin](https://www.amazon.com.br/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Python Dependency Injection](https://python-dependency-injector.ets-labs.org/)
- [Domain-Driven Design in Python](https://github.com/heynickc/dddp)

---

This reference serves as a conceptual foundation for applying Clean Architecture in Python-based projects. While the syntax and tooling differ, the core ideas remain powerful and transformative.
