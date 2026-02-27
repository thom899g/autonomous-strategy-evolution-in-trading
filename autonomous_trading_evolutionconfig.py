"""
Configuration management for autonomous trading evolution system
Centralized configuration with environment-based overrides
"""

import os
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation"""
    credential_path: str = os.getenv("FIREBASE_CREDENTIAL_PATH", "firebase-credentials.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    database_url: str = os.getenv("FIREBASE_DATABASE_URL", "")
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        if not all([self.credential_path, self.project_id, self.database_url]):
            logging.error("Firebase configuration incomplete")
            return False
        
        if not os.path.exists(self.credential_path):
            logging.error(f"Firebase credentials file not found: {self.credential_path}")
            return False
        
        return True

@dataclass
class TradingConfig:
    """Trading-specific configuration"""
    simulation_initial_balance: float = float(os.getenv("SIMULATION_BALANCE", "10000.0"))
    max_drawdown_limit: float = float(os.getenv("MAX_DRAWDOWN_LIMIT", "0.2"))  # 20%
    minimum_sharpe_ratio: float = float(os.getenv("MINIMUM_SHARPE_RATIO", "1.5"))
    backtest_lookback_days: int = int(os.getenv("BACKTEST_LOOKBACK_DAYS", "365"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.02"))  # 2%

@dataclass
class ModelConfig:
    """AI model configuration"""
    generation_batch_size: int = int(os.getenv("GENERATION_BATCH_SIZE", "10"))
    mutation_rate: float = float(os.getenv("MUTATION_RATE", "0.1"))
    crossover_rate: float = float(os.getenv("CROSSOVER_RATE", "0.7"))
    population_size: int = int(os.getenv("POPULATION_SIZE", "100"))
    elite_count: int = int(os.getenv("ELITE_COUNT", "10"))

class ConfigManager:
    """Centralized configuration manager"""
    
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.model = ModelConfig()
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        
        # Initialize logging
        self._setup_logging()
        
        # Validate critical configurations
        self._validate_configurations()
    
    def _setup_logging(self):
        """Configure logging based on environment"""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format='%(asctime)s - %(name)s - %(levelname