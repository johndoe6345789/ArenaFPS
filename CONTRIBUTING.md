# Contributing to Unreal3Arena

Thank you for your interest in contributing to Unreal3Arena! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Unreal3Arena.git
   cd Unreal3Arena
   ```

3. **Run setup script**
   ```bash
   ./setup.sh
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Prerequisites

- **Unreal Engine 5.7** installed
- **Python 3.11+** with pip
- **Git** for version control
- Text editor or IDE (VS Code, Visual Studio, Rider, etc.)

### Project Structure

```
Unreal3Arena/
├── Plugins/GameFeatures/Quake3Arena/  # Game mode plugin
│   ├── Source/                        # C++ source code
│   ├── Content/                       # Blueprints and assets
│   └── README.md                      # Plugin documentation
├── Tools/ProceduralGeneration/        # Python generators
│   ├── arena_generator.py
│   ├── weapon_generator.py
│   └── test_*.py                      # Unit tests
└── .github/workflows/                 # CI/CD pipelines
```

### Making Changes

#### C++ Code Changes

1. Make your changes in the appropriate source files
2. Follow Unreal Engine coding standards
3. Build the project in Unreal Editor
4. Test your changes

#### Python Code Changes

1. Make changes to generator scripts
2. Add/update unit tests
3. Run tests locally:
   ```bash
   cd Tools/ProceduralGeneration
   python -m pytest test_*.py -v
   ```
4. Generate assets to verify:
   ```bash
   python generate_all.py
   ```

### Testing

#### Python Tests

Run all tests:
```bash
cd Tools/ProceduralGeneration
python -m pytest -v
```

Run specific test file:
```bash
python test_arena_generator.py
```

#### Unreal Engine Tests

1. Open project in Unreal Editor
2. Run any existing automation tests
3. Manually test gameplay changes

### Code Quality

#### Python

- Follow PEP 8 style guide
- Add docstrings to functions and classes
- Keep functions focused and testable
- Add type hints where appropriate

#### C++

- Follow Unreal Engine coding standards
- Use appropriate Unreal macros (UCLASS, UFUNCTION, UPROPERTY)
- Add comments for complex logic
- Keep header files clean and minimal

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(bot): Add advanced pathfinding for bots
fix(arena): Correct platform height calculation
docs(readme): Update installation instructions
test(generator): Add tests for weapon generation
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
   ```bash
   cd Tools/ProceduralGeneration
   python -m pytest -v
   ```
4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** on GitHub
6. **Describe your changes** in the PR description
7. **Wait for review** and address any feedback

### PR Checklist

- [ ] Tests added for new features
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code follows project style guidelines
- [ ] Commits follow conventional commit format
- [ ] No merge conflicts

## Areas for Contribution

### High Priority

- **Weapon System**: Implement Q3A weapons (Rocket Launcher, Railgun, etc.)
- **Pickup System**: Health and armor pickups
- **Movement System**: Strafe jumping and bunny hopping
- **HUD**: Score display, health/armor indicators

### Medium Priority

- **Bot Improvements**: Better pathfinding, difficulty levels
- **Game Modes**: Team Deathmatch, Capture the Flag
- **Maps**: More procedural map templates
- **Effects**: Particle effects for weapons

### Low Priority

- **Powerups**: Quad Damage, Haste, etc.
- **Spectator Mode**: Watch other players
- **Demo Recording**: Record and replay matches
- **Modding Support**: Plugin system for custom content

## Code Review Process

All submissions require review before merging:

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Documentation** review if applicable

## Community Guidelines

- Be respectful and constructive
- Help others learn and improve
- Focus on the code, not the person
- Accept and provide constructive feedback
- Follow the code of conduct

## Questions?

- Open an issue for bugs or feature requests
- Join discussions in existing issues
- Check documentation first (README.md, plugin docs, etc.)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Your contributions help make Unreal3Arena better for everyone. We appreciate your time and effort!
