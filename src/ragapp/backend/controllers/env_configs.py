import logging

from backend.models.base_env import BaseEnvConfig
from create_llama.backend.app.settings import init_settings

logger = logging.getLogger(__name__)


class EnvConfigManager:
    @classmethod
    def update(
        cls,
        current_config: BaseEnvConfig,
        new_config: BaseEnvConfig,
        rollback_on_failure: bool = True,
    ):
        """
        Update the environment configuration with the provided config.

        Args:
            env_config (BaseEnvConfig): The new environment configuration.
            rollback_on_failure (bool): Whether to rollback the changes if the update fails.
        """
        # Backup the current config
        backup_config = current_config.copy()

        # Try to update the config
        try:
            new_config.to_runtime_env()
            new_config.to_env_file()
            init_settings()
        except Exception as e:
            logger.error(
                f"Failed to update the environment config: {str(e)}", exc_info=True
            )
            if rollback_on_failure:
                # Restore the backup config
                backup_config.to_runtime_env()
                backup_config.to_env_file()
                init_settings()
            raise e
