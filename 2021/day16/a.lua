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

local literal_type <const> = 4

local function parse_number(bits, index, length)
    return tonumber(bits:sub(index, index + length - 1), 2), index + length
end

local function parse_packet(bits, n)
    local version, type_id
    version, n = parse_number(bits, n, 3)
    type_id, n = parse_number(bits, n, 3)
    if type_id == literal_type then
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
            while n + 6 < end_subpackets do
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

local function version_sum(packet)
    local result = 0
    result = result + packet.version
    if packet.type_id ~= literal_type then
        for _, child in pairs(packet.subpackets) do
            result = result + version_sum(child)
        end
    end
    return result
end

local data = io.read()
local bits = ""
for a, b in data:gmatch("(.)(.)") do
    bits = bits .. mapping_table[a] .. mapping_table[b]
end

local packet = parse_packet(bits, 1)
local ans = version_sum(packet)
print(ans)
