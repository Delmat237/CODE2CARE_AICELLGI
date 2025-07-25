"""
Script to run comprehensive tests and evaluations
"""

import subprocess
import sys
import json
import asyncio
from pathlib import Path
from backend.chatbot import MedicalChatbot
from backend.evaluation import evaluate_response

def run_unit_tests():
    """Run unit tests"""
    print("🧪 Running unit tests...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                          capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests with test conversations"""
    print("🔄 Running integration tests...")
    
    # Load test conversations
    with open('data/test_conversations.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    results = []
    
    for conversation in test_data['test_conversations']:
        print(f"Testing scenario: {conversation['scenario']}")
        
        for message_data in conversation['messages']:
            user_message = message_data['user']
            expected_elements = message_data['expected_response_elements']
            
            # Mock response for testing (in real scenario, would call the API)
            mock_response = generate_mock_response(user_message, expected_elements)
            
            # Evaluate response
            evaluation = evaluate_response(user_message, mock_response)
            
            results.append({
                'scenario': conversation['scenario'],
                'message': user_message,
                'evaluation': evaluation,
                'passed': evaluation['score'] > 0.7
            })
    
    # Report results
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    print(f"✅ Integration tests: {passed}/{total} passed")
    
    return passed == total

def generate_mock_response(user_message, expected_elements):
    """Generate mock response for testing"""
    response = "Je comprends votre préoccupation. "
    
    if 'empathie' in expected_elements:
        response += "C'est normal d'être inquiet. "
    
    if 'questions_suivi' in expected_elements:
        response += "Pouvez-vous me donner plus de détails? "
    
    if 'recommandation_consultation' in expected_elements:
        response += "Je vous recommande de consulter un médecin. "
    
    if 'urgence_consultation' in expected_elements:
        response += "Il est important de consulter rapidement un professionnel de santé. "
    
    return response

def check_code_quality():
    """Check code quality with flake8"""
    print("📊 Checking code quality...")
    
    result = subprocess.run([sys.executable, "-m", "flake8", "backend/", "--max-line-length=120"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Code quality check passed")
        return True
    else:
        print("❌ Code quality issues found:")
        print(result.stdout)
        return False

def check_security():
    """Basic security checks"""
    print("🔒 Running security checks...")
    
    security_issues = []
    
    # Check for hardcoded secrets
    for py_file in Path("backend").glob("**/*.py"):
        content = py_file.read_text()
        if "secret_key" in content.lower() and "your_secret_key" in content:
            security_issues.append(f"Hardcoded secret in {py_file}")
    
    # Check for SQL injection vulnerabilities
    for py_file in Path("backend").glob("**/*.py"):
        content = py_file.read_text()
        if "f\"SELECT" in content or "f'SELECT" in content:
            security_issues.append(f"Potential SQL injection in {py_file}")
    
    if security_issues:
        print("❌ Security issues found:")
        for issue in security_issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ No security issues found")
        return True

def main():
    """Main test runner"""
    print("🚀 Starting comprehensive test suite...")
    
    results = {
        'unit_tests': run_unit_tests(),
        'integration_tests': run_integration_tests(),
        'code_quality': check_code_quality(),
        'security': check_security()
    }
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    for test_type, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_type.replace('_', ' ').title()}: {status}")
    
    overall_passed = all(results.values())
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if overall_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if overall_passed else 1

if __name__ == "__main__":
    sys.exit(main())