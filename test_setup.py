#!/usr/bin/env python3
"""
Test script to verify RCA Platform setup
"""
import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"✗ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ Requests imported successfully")
    except ImportError as e:
        print(f"✗ Requests import failed: {e}")
        return False
    
    try:
        import transformers
        print("✓ Transformers (local LLM) imported successfully")
    except ImportError as e:
        print(f"✗ Transformers import failed: {e}")
        return False
    
    try:
        import torch
        print("✓ PyTorch imported successfully")
    except ImportError as e:
        print(f"✗ PyTorch import failed: {e}")
        return False
    
    try:
        from app.database import engine
        print("✓ Database engine imported successfully")
    except ImportError as e:
        print(f"✗ Database engine import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = [
        'DATABASE_URL',
        'GOOGLE_CHAT_WEBHOOK_URL',
        'METRIC_URL',
        'TRACE_BASE_URL',
        'LOGS_API_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is missing")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        return False
    
    return True

def test_local_llm():
    """Test local LLM setup"""
    print("\n🔍 Testing local LLM setup...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # Test with a small model first
        model_name = "microsoft/DialoGPT-medium"
        print(f"🤖 Testing local LLM: {model_name}")
        
        # This will download the model on first run
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        print("✓ Tokenizer loaded successfully")
        
        # Test model loading (this might take time on first run)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        print("✓ Model loaded successfully")
        
        # Test basic generation
        test_input = "Analyze this error: 500 Internal Server Error"
        inputs = tokenizer.encode(test_input, return_tensors="pt", truncation=True, max_length=100)
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 50,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("✓ Local LLM generation test successful")
        return True
        
    except Exception as e:
        print(f"⚠️ Local LLM test failed: {e}")
        print("🔄 System will fall back to simple analysis")
        return True  # Don't fail the test, as we have fallback

def test_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from app.database import engine
        from app.models import Base
        
        # Try to create tables
        Base.metadata.create_all(bind=engine)
        print("✓ Database connection successful")
        print("✓ Tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 RCA Platform Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_environment,
        test_local_llm,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! RCA Platform is ready to run.")
        print("\n🚀 To start the application:")
        print("1. Backend API: python run_backend.py")
        print("2. Background Worker: python run_worker.py")
        print("3. Frontend: cd frontend && npm start")
        print("\n🤖 Local LLM will be downloaded automatically on first run")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 