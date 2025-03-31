配置字段说明：

    w_mode=1 工作模式，1普通工作模式；2开发模式
    ochannel=1 输出方式，1:usb 2:rs232/rs485 4:ttl 8:wifi 16：weigand 64:以太网（不包括MP86）
    nochannel=1 与ochannel保持一致
    dchannel=64 开发协议类型，仅在w_mode=2时生效。
    ndchannel=64 与ndchannel保持一致。
    de_type=1 码制选择
    owifi=1 WiFi输出使能
    devnum=114514 设备编号，這裡封裝後將ASCII字元轉成連續int
    nfc=1 NFC功能使能
    nfc_identity_card_enable=1 身份证识别使能
    nfc_card_protocol=3 卡片协议类型
    st=1 起始位
    len=8 长度
    nft=0 结束位
    awifi_s=2 WiFi服务器模式
    relayd=1000 继电器延时
    awifi_f=4 WiFi功能选择
    haddr 服务器地址
    houttime=5 超时时间
    ...
    其他详细配置字段，可以用微信扫描微光配置工具生成的二维码获得