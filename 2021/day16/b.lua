local mapping_table <const> = {
    ['0']='0000',
    ['1']='0001',
    ['2']='0010',
    ['3']='0011',
    ['4']='0100',
    ['5']='0101',
    ['6']='0110',
    ['7']='0111',
    ['8']='1000',
    ['9']='1001',
    ['A']='1010',
    ['B']='1011',
    ['C']='1100',
    ['D']='1101',
    ['E']='1110',
    ['F']='1111',
}

local op <const> = {
    SUM=0,
    PRODUCT=1,
    MIN=2,
    MAX=3,
    LITERAL=4,
    GT=5,
    LT=6,
    EQ=7,
}

local function parse_number(bits, index, length)
    local subbits = bits:sub(index, index + length - 1)
    return tonumber(subbits, 2), index + length
end

local function parse_packet(bits, n)
    local version, type_id
    version, n = parse_number(bits, n, 3)
    type_id, n = parse_number(bits, n, 3)
    if type_id == op.LITERAL then
        local number = ""
        local more_bits = "1"
        while more_bits == "1" do
            more_bits, n = bits:sub(n, n), n + 1
            number, n = number .. bits:sub(n, n + 3), n + 4
        end
        return {
            version=version,
            type_id=type_id,
            number=tonumber(number, 2),
        }, n
    else
        local length_type_id, subpackets, subpacket_bits
        length_type_id, n = bits:sub(n, n), n + 1
        subpackets = {}
        if length_type_id == "0" then
            subpacket_bits, n = parse_number(bits, n, 15), n + 15
            local end_subpackets = n + subpacket_bits
            local packet
            while n < end_subpackets do
                packet, n = parse_packet(bits, n)
                table.insert(subpackets, packet)
            end
        else
            local num_subpackets
            num_subpackets, n = parse_number(bits, n, 11), n + 11
            local packet
            for _ = 1, num_subpackets do
                packet, n = parse_packet(bits, n)
                table.insert(subpackets, packet)
            end
        end
        return {
            version=version,
            type_id=type_id,
            subpackets=subpackets,
        }, n
    end
end

local function eval(packet, indent)
    local result
    if packet.type_id == op.SUM then
        result = 0
        for _, child in pairs(packet.subpackets) do
            result = result + eval(child, indent .. ' ')
        end
    elseif packet.type_id == op.PRODUCT then
        result = 1
        for _, child in pairs(packet.subpackets) do
            result = result * eval(child, indent .. ' ')
        end
    elseif packet.type_id == op.MIN then
        result = 640 << 10  -- ought to be enough
        for _, child in pairs(packet.subpackets) do
            result = math.min(result, eval(child, indent .. ' '))
        end
    elseif packet.type_id == op.MAX then
        result = 0
        for _, child in pairs(packet.subpackets) do
            result = math.max(result, eval(child, indent .. ' '))
        end
    elseif packet.type_id == op.LITERAL then
        result = packet.number
    elseif packet.type_id == op.GT then
        local a = eval(packet.subpackets[1], indent .. ' ')
        local b = eval(packet.subpackets[2], indent .. ' ')
        if a > b then
            result = 1
        else
            result = 0
        end
    elseif packet.type_id == op.LT then
        local a = eval(packet.subpackets[1], indent .. ' ')
        local b = eval(packet.subpackets[2], indent .. ' ')
        if a < b then
            result = 1
        else
            result = 0
        end
    elseif packet.type_id == op.EQ then
        local a = eval(packet.subpackets[1], indent .. ' ')
        local b = eval(packet.subpackets[2], indent .. ' ')
        if a == b then
            result = 1
        else
            result = 0
        end
    else
        io.stderr:write(string.format("%s\n", "UNKNOWN PACKET TYPE"))
        os.exit(1)
    end
    return result
end

local data = io.read()
local bits = ""
for a, b in data:gmatch("(.)(.)") do
    bits = bits .. mapping_table[a] .. mapping_table[b]
end

local packet = parse_packet(bits, 1)
print(eval(packet, ''))
