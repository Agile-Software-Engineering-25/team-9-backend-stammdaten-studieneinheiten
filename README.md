# UserService

UserService is a Spring Boot-based application designed to manage user-related operations. It leverages modern Java (Java 21) and integrates with various Spring Boot modules for web, data, and testing functionalities.

## Features

- RESTful API for user management
- Integration with H2 in-memory database
- Dependency injection and configuration using Spring Boot
- Unit and integration testing with JUnit 5
- Maven-based build and dependency management

## Prerequisites

- Java 21 or higher
- Maven 3.8 or higher

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-repo/userservice.git
cd userservice
```
### Build the Project
```bash
mvn clean install
```
### Run the Application
```bash
mvn spring-boot:run
```
The application will start on http://localhost:8080

## Testing
### Unit Tests
Run unit tests using Maven:
```bash
mvn test
```
### System Tests
Here information will follow, but system tests will be run on a central server and reports will be made.

## Code Style & Linting

This project uses Checkstyle (CLI jar) and EditorConfig to enforce a consistent Java code style.

- How to run locally:
  - Using the bundled/dl jar:
    - Windows PowerShell:
      ```powershell
      java -jar checkstyle.jar -c checkstyle.xml -f xml -o target\checkstyle-report.xml src\main\java src\test\java
      ```
      Or, if you have `checkstyle-11.0.0-all.jar`:
      ```powershell
      java -jar checkstyle-11.0.0-all.jar -c checkstyle.xml -f xml -o target\checkstyle-report.xml src\main\java src\test\java
      ```
    - Plain, human‑readable output:
      ```powershell
      java -jar checkstyle.jar -c checkstyle.xml -f plain src\main\java src\test\java
      ```

- IDE auto-formatting:
  - `.editorconfig` sets 2‑space indentation for `*.java` and YAML, trims trailing whitespace, and enforces final newline.
  - IntelliJ import layout is aligned with our import groups.

- Checkstyle rules (high‑level):
  - Naming:
    - `TypeName`, `MethodName`, `LocalVariableName`, `MemberName`, `ConstantName`
    - Generic type parameters: `ClassTypeParameterName`, `MethodTypeParameterName`, `InterfaceTypeParameterName` (single capital letter)
  - Packages: `PackageName` (lowercase dotted segments)
  - Formatting:
    - `Indentation`: 2 spaces; continuation indent 4; tabs disallowed
    - `LeftCurly` = `eol`; `RightCurly` = `alone`
    - `MethodParamPad` = `nospace`
    - `WhitespaceAfter` for `COMMA` and control‑flow keywords
    - `OperatorWrap` enabled (default behavior)
    - `LineLength` max 80; ignores package/import/URLs
    - `ParenPad` is disabled in this config
  - Statements:
    - `NeedBraces` on all control statements
    - `FallThrough` for switch
    - `OneStatementPerLine`
  - Imports:
    - `ImportOrder` under `TreeWalker`: groups `java, javax, org, com`; `option=top`; `sortStaticImportsAlphabetically=true`
    - `UnusedImports` to flag and fail on unused imports
  - Other:
    - `MagicNumber` enabled; ignores `-1,0,1,2`, annotations, and `hashCode`

Adjust rules in `checkstyle.xml`; IDE basics are in `.editorconfig`.

## CI: GitHub Actions (Checkstyle)

We run Checkstyle in CI on every push and on PRs to `main`.

- Workflow: `.github/workflows/checkstyle.yml`
  - Sets up Temurin JDK 21
  - Uses `checkstyle-11.0.0-all.jar` (downloaded if not in repo) or `checkstyle.jar` if present
  - Runs Checkstyle against `src/main/java` and `src/test/java`
  - Fails the job on violations and uploads `target/checkstyle-report.xml` as an artifact

- Blocking PRs on failures:
  - In GitHub repo settings → Branches → Protect `main`
  - Enable “Require status checks to pass before merging”
  - Select the “Checkstyle” job as a required status check

## Dependencies
The project uses the following key dependencies:
- `spring-boot-starter-web`: For building web applications, including RESTful services.
- `spring-boot-starter-data-jpa`: For integrating with JPA and databases.
- `spring-boot-starter-test`: For testing support, including JUnit 5.
- `h2`: An in-memory database for development and testing purposes.
- `lombok`: For reducing boilerplate code in Java classes.
- `spring-boot-starter-validation`: For validating user input.
- `spring-boot-starter-security`: For securing the application with basic authentication.
- `springdoc-openapi-ui`: For generating OpenAPI documentation and Swagger UI.
- `spring-boot-starter-actuator`: For monitoring and managing the application.


## Security && rbac
Endpoint Access/Security is configured in package com.ase.userservice.security via SecurityConfig.java.

To add a new rule, you need to fill the function parameters for this snippet:
```java
http
  .authorizeHttpRequests(authorize -> authorize
    .requestMatchers("/demo").hasRole("DEFAULT-ROLES-SAU")
    .requestMatchers("/admin/**").hasRole("admin")
    .anyRequest().authenticated()
  )
  .oauth2ResourceServer(oauth2 -> oauth2
    .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtConverter))
  );
```

Specifically you need to add the following line for each protected route and role:
```java
.requestMatchers("/<your-route>").hasRole("<your-role>")
```
Glob pattern matching is supported.

If you need more infos regarding secuirty, visit our documentation page: [placeholder](http://example.com)