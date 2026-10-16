"""SQLAlchemy models."""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CobolProgram(Base):
    __tablename__ = 'cobol_programs'
    id = Column(Integer, primary_key=True)
    program_id = Column(String, unique=True, nullable=False)
    source_language = Column(String)
    source_repo = Column(String)
    source_license = Column(String)
    generated_cobol = Column(Text)
    generated_java_back = Column(Text)
    domain = Column(String)
    complexity_score = Column(Float)
    loc_count = Column(Integer)
    validation_status = Column(String)
    created_at = Column(String)

class CobolParagraph(Base):
    __tablename__ = 'cobol_paragraphs'
    id = Column(Integer, primary_key=True)
    program_fk = Column(Integer, ForeignKey('cobol_programs.id'))
    paragraph_name = Column(String)
    cobol_snippet = Column(Text)
    business_description_ar = Column(Text)
    business_description_en = Column(Text)
    java_equivalent = Column(Text)

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    program_fk = Column(Integer, ForeignKey('cobol_programs.id'))
    input_data = Column(JSON)
    expected_output = Column(JSON)
    cobol_output = Column(JSON)
    validation_passed = Column(Boolean)

class LegalProvenance(Base):
    __tablename__ = 'legal_provenance'
    id = Column(Integer, primary_key=True)
    program_fk = Column(Integer, ForeignKey('cobol_programs.id'))
    source_license = Column(String)
    transformation_method = Column(String)
    llm_model = Column(String)
    prompt_version = Column(String)
    validation_evidence = Column(Text)

class BenchmarkTask(Base):
    __tablename__ = 'benchmark_tasks'
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True)
    instruction_prompt = Column(Text)
    complete_prompt = Column(Text)
    canonical_solution = Column(Text)
    input_files = Column(JSON)
    output_files = Column(JSON)
    expected_output = Column(JSON)
