import bincopy
import configparser


def srec_open(fname):
    f = bincopy.BinFile(fname)
    return f.as_binary(0)

def bin_open(fname):
    with open(fname, 'rb') as f:
        barray = f.read()

    return barray


def rerange(mcu, bin, config):
    f = bincopy.BinFile()
    map = config[mcu.lower()]
    offset = 0
    for i in map:
        if i[:2] == 'of':
            offset = int(map[i], 16)
            startadr = offset
            f.add_binary([0xff for _ in range(offset)])
        elif i[:2] == 'st':
            start = map[i]
        elif i[:2] == 'en':
            page = bin[int(start, 16):int(map[i], 16) + 1]
            f.add_binary(page, offset)
            offset += len(page)
        elif i[:2] == 'si':
            page = bin[int(start, 16):int(map[i], 16) + int(start, 16)]
            f.add_binary(page, offset)
            offset += len(page)
    #f.exclude(0,startadr)
    return f


def bin_save(fname, ftype, bin):
    fname = fname.partition('.')[0] + '_good' + ftype
    if ftype == '.bin':
        with open(fname, 'wb') as f:
            f.write(bin.as_binary())
    elif ftype == '.s19':
        with open(fname, 'w') as f:
            f.write(bin.as_srec(14,24))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('maps.ini')
    bin = srec_open('9000781283.s2')
    out = rerange('mc9s12c128', bin, config)
    bin_save('bad2.bin', '.s19', out)
