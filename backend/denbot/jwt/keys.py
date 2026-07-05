import base64
import hashlib
import json
from functools import cached_property
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PrivateFormat,
    NoEncryption,
)
from jwt.algorithms import RSAAlgorithm


class JWTSigningKeys:
    def __init__(self, keys_dir: Path, generate_missing_key: bool):
        self._keys_dir: Path = keys_dir
        self._generate_missing_key: bool = generate_missing_key

    @cached_property
    def _private_key(self) -> PrivateKeyTypes:
        pem_files = sorted(self._keys_dir.glob("*.pem"))
        if len(pem_files) == 1:
            return serialization.load_pem_private_key(
                pem_files[0].read_bytes(), password=None
            )

        if len(pem_files) > 1:
            raise RuntimeError(
                f"multiple signing keys in {self._keys_dir}: {[p.name for p in pem_files]}"
            )

        # No pem_files at this point
        if not self._generate_missing_key:
            raise RuntimeError(f"no signing key in {self._keys_dir}")

        return self._generate_key()

    def _generate_key(self) -> PrivateKeyTypes:
        rsa_key: RSAPrivateKey = rsa.generate_private_key(
            public_exponent=65537, key_size=2048
        )

        pem_data = rsa_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        )

        dev_key_path = self._keys_dir / "auto-generated.pem"

        with dev_key_path.open("wb") as fh:
            fh.write(pem_data)

        return rsa_key

    @cached_property
    def signing_key_pem(self) -> str:
        return self._private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

    @cached_property
    def verifying_key_pem(self) -> str:
        return (
            self._private_key.public_key()
            .public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode()
        )

    @cached_property
    def _public_jwk(self) -> dict:  # {"kty","n","e"}
        # noinspection PyTypeChecker
        return RSAAlgorithm.to_jwk(self._private_key.public_key(), as_dict=True)

    @cached_property
    def key_id(self) -> str:  # RFC 7638 thumbprint
        jwk = self._public_jwk
        members = {
            "e": jwk["e"],
            "kty": jwk["kty"],
            "n": jwk["n"],
        }  # required set, sorted
        canonical = json.dumps(members, separators=(",", ":"), sort_keys=True).encode()
        return (
            base64.urlsafe_b64encode(hashlib.sha256(canonical).digest())
            .rstrip(b"=")
            .decode()
        )

    @cached_property
    def jwks(self) -> dict:
        return {
            "keys": [
                {**self._public_jwk, "kid": self.key_id, "use": "sig", "alg": "RS256"}
            ]
        }
