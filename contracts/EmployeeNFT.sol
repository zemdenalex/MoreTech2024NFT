// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

<<<<<<< HEAD
import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "node_modules/@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EmployeeNFT
 * @dev Смарт-контракт для управления информацией о сотрудниках и выпуска soulbound NFT на сети Arbitrum, соответствующий стандарту ERC-721
 */
contract EmployeeNFT is ERC721, Ownable {
=======
/**
 * @title EmployeeNFT
 * @dev Смарт-контракт для управления информацией о сотрудниках и выпуска soulbound NFT с генерируемым хэшем для обеспечения подлинности
 */
contract EmployeeNFT {
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
    // Определение структуры для хранения данных о сотруднике
    struct EmployeeData {
        address recipientAddress;
        string image;
        string text;
        uint256 timeStamp;
        string[] tags;
        bool isApproveNFT;
        string reason;
<<<<<<< HEAD
        uint256 previousTokenId;
=======
        address previousNFTAddress;
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        bytes32 dataHash;
    }

    // Отображение tokenId на EmployeeData
    mapping(uint256 => EmployeeData) private employeeData;

<<<<<<< HEAD
    // Счетчик для отслеживания количества выпущенных NFT
    uint256 public tokenCounter;

    // Объявление события для выпуска нового NFT
    event EmployeeNFTMinted(uint256 indexed tokenId, address indexed recipientAddress);

    /**
     * @dev Конструктор для инициализации счетчика токенов
     */
    constructor() ERC721("EmployeeNFT", "ENFT") {
=======
    // Отображение для хранения владения soulbound NFT
    mapping(uint256 => address) private tokenOwner;

    // Событие, которое эмитируется при выпуске нового NFT
    event EmployeeNFTMinted(uint256 indexed tokenId, address indexed recipientAddress);

    // Счетчик для отслеживания количества выпущенных NFT
    uint256 public tokenCounter; // Оставляем как есть, Solidity автоматически создаст геттер.

    /**
     * @dev Конструктор для инициализации счетчика токенов
     */
    constructor() {
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        tokenCounter = 0; // Инициализация счетчика токенов
    }

    /**
     * @dev                         Function to generate a hash from employee data
     * @dev                         Функция для генерации хэша из данных о сотруднике
<<<<<<< HEAD
=======
     * @param _recipientAddress     Address of the recipient / Адрес получателя
     * @param _image                Image link (IPFS or other storage) / Ссылка на изображение (IPFS или другое хранилище)
     * @param _text                 General text about the employee / Общая информация о сотруднике в текстовом формате
     * @param _timeStamp            Timestamp of the record / Временная метка записи
     * @param _tags                 Array of tags associated with the employee / Массив тегов, связанных с сотрудником
     * @param _isApproveNFT         Boolean value indicating approval / Булево значение, указывающее на одобрение
     * @param _reason               Причина создания NFT / Reason for creating NFT
     * @param _previousNFTAddress   Адрес предыдущего NFT / Address of the previous NFT
     * @return bytes32              Сгенерированный хэш / The generated hash
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
     */
    function generateDataHash(
        address _recipientAddress,
        string memory _image,
        string memory _text,
        uint256 _timeStamp,
        string[] memory _tags,
        bool _isApproveNFT,
        string memory _reason,
<<<<<<< HEAD
        uint256 _previousTokenId
    ) public pure returns (bytes32) {
        // Комбинируем все данные в единый хэш
=======
        address _previousNFTAddress
    ) public pure returns (bytes32) {
        // Combine all data into a single hash / Комбинируем все данные в единый хэш
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        return keccak256(abi.encode(
            _recipientAddress,
            _image,
            _text,
            _timeStamp,
            _tags,
            _isApproveNFT,
            _reason,
<<<<<<< HEAD
            _previousTokenId
=======
            _previousNFTAddress
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        ));
    }

    /**
     * @dev                         Function to mint a new employee soulbound NFT
     * @dev                         Функция для выпуска нового soulbound NFT сотрудника
<<<<<<< HEAD
=======
     * @param _recipientAddress     Address of the recipient / Адрес получателя
     * @param _image                Ссылка на изображение (IPFS или другое хранилище) / Image link (IPFS or other storage)
     * @param _text                 Общая информация о сотруднике в текстовом формате / General text about the employee
     * @param _timeStamp            Временная метка записи / Timestamp of the record
     * @param _tags                 Массив тегов, связанных с сотрудником / Array of tags associated with the employee
     * @param _isApproveNFT         Булево значение, указывающее на одобрение / Boolean value indicating approval
     * @param _reason               Причина создания NFT / Reason for creating NFT
     * @param _previousNFTAddress   Адрес предыдущего NFT / Address of the previous NFT
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
     */
    function mintEmployeeNFT(
        address _recipientAddress,
        string memory _image,
        string memory _text,
        uint256 _timeStamp,
        string[] memory _tags,
        bool _isApproveNFT,
        string memory _reason,
<<<<<<< HEAD
        uint256 _previousTokenId
    ) public onlyOwner {
        // Генерация хэша из предоставленных данных
=======
        address _previousNFTAddress
    ) public {
        // Generate a hash from the provided data / Генерация хэша из предоставленных данных
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        bytes32 dataHash = generateDataHash(
            _recipientAddress,
            _image,
            _text,
            _timeStamp,
            _tags,
            _isApproveNFT,
            _reason,
<<<<<<< HEAD
            _previousTokenId
        );

        // Кэшируем значение tokenCounter для уменьшения обращений к хранилищу
        uint256 currentTokenId = tokenCounter;

        // Создание новой структуры данных сотрудника
        employeeData[currentTokenId] = EmployeeData({
=======
            _previousNFTAddress
        );

        // Create new employee data struct / Создание новой структуры данных сотрудника
        EmployeeData memory newEmployeeData = EmployeeData({
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
            recipientAddress: _recipientAddress,
            image: _image,
            text: _text,
            timeStamp: _timeStamp,
            tags: _tags,
            isApproveNFT: _isApproveNFT,
            reason: _reason,
<<<<<<< HEAD
            previousTokenId: _previousTokenId,
            dataHash: dataHash
        });

        // Выпуск NFT с использованием функции OpenZeppelin _safeMint
        _safeMint(_recipientAddress, currentTokenId);

        // Эмитируем событие, указывающее, что выпущен новый NFT
        emit EmployeeNFTMinted(currentTokenId, _recipientAddress);

        // Увеличиваем счетчик токенов для следующего выпуска
=======
            previousNFTAddress: _previousNFTAddress,
            dataHash: dataHash
        });

        // Store the employee data in the mapping / Сохранение данных сотрудника в отображении
        employeeData[tokenCounter] = newEmployeeData;

        // Store the ownership of the soulbound NFT / Сохранение владения soulbound NFT
        tokenOwner[tokenCounter] = _recipientAddress;

        // Emit an event indicating a new NFT is minted / Эмитируем событие, указывающее, что выпущен новый NFT
        emit EmployeeNFTMinted(tokenCounter, _recipientAddress);

        // Increment the token counter for the next mint / Увеличиваем счетчик токенов для следующего выпуска
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        tokenCounter++;
    }

    /**
     * @dev                 Function to get employee data by tokenId
     * @dev                 Функция для получения данных сотрудника по идентификатору токена
<<<<<<< HEAD
     */
    function getEmployeeData(uint256 _tokenId) public view returns (EmployeeData memory) {
        require(_exists(_tokenId), "Token ID does not exist");
=======
     * @param _tokenId      Идентификатор токена для получения данных / The ID of the token to retrieve data for
     * @return EmployeeData Данные запрашиваемого NFT сотрудника / The data of the requested employee NFT
     */
    function getEmployeeData(uint256 _tokenId) public view returns (EmployeeData memory) {
        require(_tokenId < tokenCounter, "Token ID does not exist"); // Ensure token ID is valid / Убедитесь, что идентификатор токена действителен
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
        return employeeData[_tokenId];
    }

    /**
     * @dev                 Function to prevent transferring soulbound NFTs
     * @dev                 Функция для предотвращения передачи soulbound NFT
<<<<<<< HEAD
     */
    function _transfer(address, address, uint256) internal pure override {
        revert("Soulbound NFTs cannot be transferred");
    }
}
=======
     * @param _tokenId      Идентификатор токена / The ID of the token to prevent transfer
     */
    function _transfer(address from, address to, uint256 _tokenId) internal pure {
        revert("Soulbound NFTs cannot be transferred"); // Soulbound NFTs are non-transferable / Soulbound NFT нельзя передавать
    }

    /**
     * @dev                 Override transfer functions to disable transfer
     * @dev                 Переопределение функций передачи для отключения передачи
     * @param from          Адрес отправителя / The address of the sender
     * @param to            Адрес получателя / The address of the recipient
     * @param tokenId       Идентификатор токена / The ID of the token to be transferred
     */
    function transferFrom(address from, address to, uint256 tokenId) public pure {
        _transfer(from, to, tokenId);
    }

    /**
     * @dev                 Override safe transfer functions to disable transfer
     * @dev                 Переопределение безопасной передачи для отключения передачи
     * @param from          Адрес отправителя / The address of the sender
     * @param to            Адрес получателя / The address of the recipient
     * @param tokenId       Идентификатор токена / The ID of the token to be transferred
     */
    function safeTransferFrom(address from, address to, uint256 tokenId) public pure {
        _transfer(from, to, tokenId);
    }

    /**
     * @dev                 Override safe transfer functions with data to disable transfer
     * @dev                 Переопределение безопасной передачи с данными для отключения передачи
     * @param from          Адрес отправителя / The address of the sender
     * @param to            Адрес получателя / The address of the recipient
     * @param tokenId       Идентификатор токена / The ID of the token to be transferred
     * @param _data         Дополнительные данные / Additional data
     */
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public pure {
        _transfer(from, to, tokenId);
    }
}
>>>>>>> 2a986e2bde83a84176b28a3848f6d3ebcddf517f
