// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "node_modules/@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EmployeeNFT
 * @dev Смарт-контракт для управления информацией о сотрудниках и выпуска soulbound NFT на сети Arbitrum, соответствующий стандарту ERC-721
 */
contract EmployeeNFT is ERC721, Ownable {
    // Определение структуры для хранения данных о сотруднике
    struct EmployeeData {
        address recipientAddress;
        string image;
        string text;
        uint256 timeStamp;
        string[] tags;
        bool isApproveNFT;
        string reason;
        uint256 previousTokenId;
        string dataHashFromBackend;
        bytes32 dataHash;
    }

    // Отображение tokenId на EmployeeData
    mapping(uint256 => EmployeeData) private employeeData;

    // Счетчик для отслеживания количества выпущенных NFT
    uint256 public tokenCounter;

    // Объявление события для выпуска нового NFT
    event EmployeeNFTMinted(uint256 indexed tokenId, address indexed recipientAddress);

    /**
     * @dev Конструктор для инициализации счетчика токенов
     */
    constructor() ERC721("EmployeeNFT", "ENFT") {
        tokenCounter = 0; // Инициализация счетчика токенов
    }

    /**
     * @dev                         Function to generate a hash from employee data
     * @dev                         Функция для генерации хэша из данных о сотруднике
     */
    function generateDataHash(
        address _recipientAddress,
        string memory _image,
        string memory _text,
        uint256 _timeStamp,
        string[] memory _tags,
        bool _isApproveNFT,
        string memory _reason,
        uint256 _previousTokenId,
        string _dataHashFromBackend
    ) public pure returns (bytes32) {
        // Комбинируем все данные в единый хэш
        return keccak256(abi.encode(
            _recipientAddress,
            _image,
            _text,
            _timeStamp,
            _tags,
            _isApproveNFT,
            _reason,
            _previousTokenId,
            _dataHashFromBackend
        ));
    }

    /**
     * @dev                         Function to mint a new employee soulbound NFT
     * @dev                         Функция для выпуска нового soulbound NFT сотрудника
     */
    function mintEmployeeNFT(
        address _recipientAddress,
        string memory _image,
        string memory _text,
        uint256 _timeStamp,
        string[] memory _tags,
        bool _isApproveNFT,
        string memory _reason,
        uint256 _previousTokenId,
        string dataHashFromBackend
    ) public onlyOwner {
        // Генерация хэша из предоставленных данных
        bytes32 dataHash = generateDataHash(
            _recipientAddress,
            _image,
            _text,
            _timeStamp,
            _tags,
            _isApproveNFT,
            _reason,
            _previousTokenId,
            _dataHashFromBackend
        );

        // Кэшируем значение tokenCounter для уменьшения обращений к хранилищу
        uint256 currentTokenId = tokenCounter;

        // Создание новой структуры данных сотрудника
        employeeData[currentTokenId] = EmployeeData({
            recipientAddress: _recipientAddress,
            image: _image,
            text: _text,
            timeStamp: _timeStamp,
            tags: _tags,
            isApproveNFT: _isApproveNFT,
            reason: _reason,
            previousTokenId: _previousTokenId,
            dataHashFromBackend: _dataHashFromBackend,
            dataHash: dataHash
        });

        // Выпуск NFT с использованием функции OpenZeppelin _safeMint
        _safeMint(_recipientAddress, currentTokenId);

        // Эмитируем событие, указывающее, что выпущен новый NFT
        emit EmployeeNFTMinted(currentTokenId, _recipientAddress);

        // Увеличиваем счетчик токенов для следующего выпуска
        tokenCounter++;
    }

    /**
     * @dev                 Function to get employee data by tokenId
     * @dev                 Функция для получения данных сотрудника по идентификатору токена
     */
    function getEmployeeData(uint256 _tokenId) public view returns (EmployeeData memory) {
        require(_exists(_tokenId), "Token ID does not exist");
        return employeeData[_tokenId];
    }

    /**
     * @dev                 Function to prevent transferring soulbound NFTs
     * @dev                 Функция для предотвращения передачи soulbound NFT
     */
    function _transfer(address, address, uint256) internal pure override {
        revert("Soulbound NFTs cannot be transferred");
    }
}
