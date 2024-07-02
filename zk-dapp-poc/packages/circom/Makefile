CIRCUITS_PATH=circuits
CONTRACTS_PATH=contracts
CIRCUIT=

clear-circom-build: 
	rm -rf $(CIRCUITS_PATH)/$(CIRCUIT)/build && mkdir $(CIRCUITS_PATH)/$(CIRCUIT)/build

clear-verifier-build:
	rm -rf $(CONTRACTS)/$(CIRCUIT)/verifier && mkdir -p $(CONTRACTS_PATH)/$(CIRCUIT)/verifier

circom-compile: clear-circom-build
	circom --r1cs --wasm --sym -l ../../node_modules/circomlib/circuits -o $(CIRCUITS_PATH)/$(CIRCUIT)/build $(CIRCUITS_PATH)/$(CIRCUIT)/$(CIRCUIT).circom

snarkjs-zkey:
	snarkjs plonk setup $(CIRCUITS_PATH)/$(CIRCUIT)/build/$(CIRCUIT).r1cs $(CIRCUITS_PATH)/_ptau/powersOfTau28_hez_final_10.ptau $(CIRCUITS_PATH)/$(CIRCUIT)/build/proving_key.zkey

snarkjs-verifier: clear-verifier-build
	snarkjs zkey export solidityverifier $(CIRCUITS_PATH)/$(CIRCUIT)/build/proving_key.zkey $(CONTRACTS_PATH)/$(CIRCUIT)/verifier/PlonkVerifier.sol