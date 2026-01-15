#### 1. Core Identity & Stack

- **Domain:** Business Process Automation.
    
- **Primary Stack:** Python 3.12+ / Django 5.x / PostgreSQL.
    
- **Frontend:** HTML5 + HTMX + Vanilla JS (for specific UX enhancements).
    
- **Styling:** Vanilla CSS (No build step). Semantic class naming managed by LLM.
    
- **Third-Party Whitelist:**
    
    - django-environ: For .env management.
        
    - django-extensions: For shell_plus and debugging tools.
        
    - whiteoise: For serving static files efficiently without Nginx complexity.
        
    - sentry-sdk: For error monitoring.
        
    - pytest-django: For the test runner.
        

#### 2. Design Philosophies & Architectural Principles

- **Schema First:** **STRICT RULE.** No UI or View logic begins until models.py is defined. Database integrity is the blocker.
    
- **Monolith Modularization:**
    
    - Use a single core app for the majority of the logic to reduce overhead.
        
    - **Folder-based separation:** As files grow, split services.py into a services/ package (e.g., services/document_logic.py).
        
- **Service Layer Pattern:**
    
    - **Thin Views:** Views only handle request reception and response rendering.
        
    - **Rich Services:** All business logic (calculations, external API calls, state transitions) lives in core/services/.
        
- **Inheritance Strategy:** All models must inherit from core.models.TimeStampedModel (abstract base class with created_at, updated_at) to ensure auditability.
    
- **Testing ROI:** Prioritize **Integration Tests** (End-to-End flows) over granular Unit Tests. Test the "Golden Path" (e.g., User creates Case -> Case Saved -> Email Sent).

#### 4. Coding Standards

- **Naming:** Verbose and descriptive (calculate_statutory_deadline > calc_date).
    
- **Import Order:**
    
    1. Standard Lib (os, datetime)
        
    2. Django Core (django.db, django.shortcuts)
        
    3. Third Party (rest_framework, sentry_sdk)
        
    4. Local Apps (core.models, core.services)
        
- **Security:**
    
    - Never hardcode secrets. Use os.environ2.get().
        
    - Never use mark_safe on user input.
        
- **JS Strategy:** Use document.querySelector and standard Event Listeners. No jQuery. Enhance forms (e.g., validation) but rely on Django POST for state changes.