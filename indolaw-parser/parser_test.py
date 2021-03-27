from parser_types import Structure, ComplexNode
from parser_utils import (
    get_squashed_list_item,
    ignore_line,
    get_list_index_type,
    get_list_index_as_num,
    is_next_list_index_number,
    clean_law,
    get_next_list_index,
    roman_to_int,
    clean_maybe_list_item
)
from parser_is_start_of_x import (
    is_heading,
    is_start_of_first_list_index,
    is_start_of_number_with_brackets_str,
    is_start_of_number_with_brackets,
    is_start_of_number_with_dot_str,
    is_start_of_number_with_dot,
    is_start_of_letter_with_dot_str,
    is_start_of_letter_with_dot,
    is_start_of_list_index,
    is_start_of_list_item,
    is_start_of_list,
    is_start_of_bab_title,
    is_start_of_bab_number,
    is_start_of_bab,
    is_start_of_paragraf_title,
    is_start_of_paragraf_number,
    is_start_of_paragraf,
    is_start_of_bagian_title,
    is_start_of_bagian_number,
    is_start_of_bagian,
    is_start_of_pasal_number,
    is_start_of_pasal,
    is_start_of_agreement,
    is_start_of_principles,
    is_start_of_considerations,
    is_start_of_preface,
    is_start_of_uu_title_topic,
    is_start_of_uu_title_year_and_number,
    is_start_of_uu_title,
    is_start_of_opening,
    is_start_of_undang_undang,
    is_start_of_any,
    is_start_of_structure
)
import pytest


def test_roman_to_int():
    assert roman_to_int('VI') == 6
    assert roman_to_int('XXI') == 21
    assert roman_to_int('LIV') == 54


def test_is_heading():
    assert is_heading('BAB [0-9]+', '  BAB 23   ')
    assert not is_heading('BAB [0-9]+', 'dengan BAB 23   ')
    assert not is_heading('BAB [0-9]+', '  asdf   ')


def test_ignore_line():
    assert ignore_line('. . .')
    assert ignore_line('5 / 23')
    assert ignore_line('- 12 -')
    assert ignore_line('www.hukumonline.com')
    assert not ignore_line('Mengingat bahwa UU No. 14...')


def test_get_list_index_type():
    assert get_list_index_type('a.') == Structure.LETTER_WITH_DOT
    assert get_list_index_type('(2)') == Structure.NUMBER_WITH_BRACKETS
    assert get_list_index_type('3.') == Structure.NUMBER_WITH_DOT
    assert get_list_index_type('cara berpikir kreatif') == None
    assert get_list_index_type('a. cara berpikir kreatif') == None


def test_get_list_index_as_num():
    assert get_list_index_as_num('d.') == 4
    assert get_list_index_as_num('13.') == 13
    assert get_list_index_as_num('(8)') == 8
    with pytest.raises(Exception):
        get_list_index_as_num('Berhubungan dengan peraturan...')


def test_is_next_list_index_number():
    assert is_next_list_index_number('d.', 'e.') == True
    assert is_next_list_index_number('(13)', '(14)') == True
    assert is_next_list_index_number('(13)', '(15)') == False
    with pytest.raises(Exception):
        is_next_list_index_number('a.', '(2)')


def test_clean_law():
    input = [
        '1 / 10',
        'Pasal 1',
        '. . .',
        'Dalam Undang-Undang in yang dimaksud dengan makanan enak adalah: 1. martabak;',
        '2. nasi goreng; 3. bakmie ayam;',
        '4. soto betawi;',
        '5. ronde jahe; 6. gulai kambing; 7. sup ikan batam;',
        '(1) Dalam Undang-Undang in yang dimaksud dengan makanan enak adalah: 1. martabak;',
        '- 2 -',
    ]
    output = [
        'Pasal 1',
        'Dalam Undang-Undang in yang dimaksud dengan makanan enak adalah:',
        '1.',
        'martabak;',
        '2.',
        'nasi goreng;',
        '3.',
        'bakmie ayam;',
        '4.',
        'soto betawi;',
        '5.',
        'ronde jahe;',
        '6.',
        'gulai kambing;',
        '7.',
        'sup ikan batam;',
        '(1)',
        'Dalam Undang-Undang in yang dimaksud dengan makanan enak adalah:',
        '1.',
        'martabak;',
    ]
    assert clean_law(input) == output


def test_is_start_of_first_list_index():
    assert is_start_of_first_list_index('a.') == True
    assert is_start_of_first_list_index('b.') == False
    assert is_start_of_first_list_index('1.') == True
    assert is_start_of_first_list_index('2.') == False
    assert is_start_of_first_list_index('(1)') == True
    assert is_start_of_first_list_index('(2)') == False
    assert is_start_of_first_list_index('dengan adanya...') == False


def test_is_start_of_number_with_brackets_str():
    assert is_start_of_number_with_brackets_str('(2)') == True
    assert is_start_of_number_with_brackets_str('b.') == False


def test_is_start_of_number_with_brackets():
    law = [
        '(1)',
        'dengan adanya...',
        '(2)',
    ]
    assert is_start_of_number_with_brackets(law, 0) == True
    assert is_start_of_number_with_brackets(law, 1) == False
    assert is_start_of_number_with_brackets(law, 2) == True


def test_is_start_of_number_with_dot_str():
    assert is_start_of_number_with_dot_str('2.') == True
    assert is_start_of_number_with_dot_str('b.') == False


def test_is_start_of_number_with_dot():
    law = [
        '1.',
        'dengan adanya...',
        '2.',
    ]
    assert is_start_of_number_with_dot(law, 0) == True
    assert is_start_of_number_with_dot(law, 1) == False
    assert is_start_of_number_with_dot(law, 2) == True


def test_is_start_of_letter_with_dot_str():
    assert is_start_of_letter_with_dot_str('b.') == True
    assert is_start_of_letter_with_dot_str('3.') == False


def test_is_start_of_letter_with_dot():
    law = [
        'a.',
        'dengan adanya...',
        'b.',
    ]
    assert is_start_of_letter_with_dot(law, 0) == True
    assert is_start_of_letter_with_dot(law, 1) == False
    assert is_start_of_letter_with_dot(law, 2) == True


def test_is_start_of_list_index():
    law = [
        'a.',
        'dengan adanya...',
        '2.',
        'dengan adanya...',
        '(3)',
        'dengan adanya...',
    ]
    assert is_start_of_list_index(law, 0) == True
    assert is_start_of_list_index(law, 1) == False
    assert is_start_of_list_index(law, 2) == True
    assert is_start_of_list_index(law, 4) == True


def test_is_start_of_list_item():
    law = [
        'Undang-Undang ini bertujuan untuk:',
        'a.',
        'menjamin hak warga negara...',
    ]

    assert is_start_of_list_item(law, 0) == False
    assert is_start_of_list_item(law, 1) == True
    assert is_start_of_list_item(law, 2) == False


def test_is_start_of_list():
    law = [
        'Pasal 4',
        'Undang-Undang ini bertujuan untuk:',
        'a.',
        'menjamin hak warga negara...',
        'b.',
        'mendorong partisipasi...',
    ]

    assert is_start_of_list(law, 1) == False
    assert is_start_of_list(law, 2) == True
    assert is_start_of_list(law, 4) == False


def test_is_start_of_bab_title():
    law = [
        'Untuk mewujudkan...',
        'BAB II',
        'ASAS DAN TUJUAN',
        'Pasal 1',
        'Kewajiban...',
    ]

    assert is_start_of_bab_title(law, 1) == False
    assert is_start_of_bab_title(law, 2) == True
    assert is_start_of_bab_title(law, 3) == False


def test_is_start_of_bab_number():
    law = [
        'BAB XIV',
        'KOMISI INFORMASI',
        'Pasal 23',
    ]

    assert is_start_of_bab_number(law, 0) == True
    assert is_start_of_bab_number(law, 1) == False


def test_is_start_of_bab():
    law = [
        'Ketentuan lebih lanjut...',
        'BAB XIV',
        'KOMISI INFORMASI',
        'Pasal 23',
    ]

    assert is_start_of_bab(law, 0) == False
    assert is_start_of_bab(law, 1) == True


def test_is_start_of_paragraf_title():
    law = [
        'Paragraf 2',
        'Izin Berusaha',
        'Pasal 5',
        'Badan hukum yang...',
    ]

    assert is_start_of_paragraf_title(law, 0) == False
    assert is_start_of_paragraf_title(law, 1) == True
    assert is_start_of_paragraf_title(law, 2) == False


def test_is_start_of_paragraf_number():
    law = [
        'Dalam hal kegiatan...',
        'Paragraf 2',
        'Izin Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_paragraf_number(law, 0) == False
    assert is_start_of_paragraf_number(law, 1) == True
    assert is_start_of_paragraf_number(law, 2) == False


def test_is_start_of_paragraf():
    law = [
        'Ketentuan lebih lanjut...',
        'Paragraf 2',
        'Perizinan Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_paragraf(law, 0) == False
    assert is_start_of_paragraf(law, 1) == True


def test_is_start_of_bagian_title():
    law = [
        'Bagian Ketiga',
        'Persyaratan Dasar',
        'Pasal 18',
        'Sesuai dengan...',
    ]

    assert is_start_of_bagian_title(law, 0) == False
    assert is_start_of_bagian_title(law, 1) == True


def test_is_start_of_bagian_number():
    law = [
        'Dalam hal kegiatan...',
        'Bagian Keempat',
        'Izin Berusaha',
        'Pasal 15',
    ]

    assert is_start_of_bagian_number(law, 0) == False
    assert is_start_of_bagian_number(law, 1) == True
    assert is_start_of_bagian_number(law, 2) == False


def test_is_start_of_bagian():
    law = [
        'Ketentuan lebih lanjut...',
        'Bagian Ketujuh',
        'Perizinan Berusaha',
        'Pasal 5',
    ]

    assert is_start_of_bagian(law, 0) == False
    assert is_start_of_bagian(law, 1) == True


def test_is_start_of_pasal_number():
    law = [
        'BAB IV',
        'Persyaratan Dasar',
        'Pasal 18',
        'Sesuai dengan...',
    ]

    assert is_start_of_pasal_number(law, 2) == True
    assert is_start_of_pasal_number(law, 3) == False


def test_is_start_of_pasal():
    law = [
        'Ketentuan lebih lanjut...',
        'Pasal 12',
        'Perizinan Berusaha',
    ]

    assert is_start_of_pasal(law, 0) == False
    assert is_start_of_pasal(law, 1) == True


def test_is_start_of_agreement():
    law = [
        'Dengan Persetujuan Bersama:',
        'DEWAN PERWAKILAN RAKYAT REPUBLIK INDONESIA',
        'dan',
        'PRESIDEN REPUBLIK INDONESIA',
        'MEMUTUSKAN:',
        'Menetapkan:',
        'UNDANG-UNDANG TENTANG KETERBUKAAN INFORMASI PUBLIK',
    ]

    assert is_start_of_agreement(law, 0) == True
    assert is_start_of_agreement(law, 1) == False


def test_is_start_of_principles():
    law = [
        'Mengingat:',
        'Pasal 20 Undang-Undang Dasar Negara Republik Indonesia Tahun 1945.',
    ]

    assert is_start_of_principles(law, 0) == True
    assert is_start_of_principles(law, 1) == False


def test_is_start_of_considerations():
    law = [
        'Menimbang:',
        'a. bahwa informasi...',
        'b. bahwa hak...',
        'c. bahwa keterbukaan...',
    ]

    assert is_start_of_considerations(law, 0) == True
    assert is_start_of_considerations(law, 1) == False


def test_is_start_of_preface():
    law = [
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
        'Menimbang:',
        'a. bahwa keterbukaan...',
    ]

    assert is_start_of_preface(law, 0) == True
    assert is_start_of_preface(law, 1) == False


def test_is_start_of_uu_title_topic():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title_topic(law, 3) == True
    assert is_start_of_uu_title_topic(law, 4) == False


def test_is_start_of_uu_title_year_and_number():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title_year_and_number(law, 1) == True


def test_is_start_of_uu_title():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_uu_title(law, 0) == True


def test_is_start_of_opening():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_opening(law, 0) == True


def test_is_start_of_undang_undang():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_undang_undang(law, 0) == True


def test_is_start_of_any():
    law = [
        'UNDANG-UNDANG REPUBLIK INDONESIA',
        'NOMOR 14 TAHUN 2008',
        'TENTANG',
        'KETERBUKAAN INFORMASI PUBLIK',
        'DENGAN RAHMAT TUHAN YANG MAHA ESA',
        'PRESIDEN REPUBLIK INDONESIA,',
    ]

    assert is_start_of_any(
        [Structure.UU_TITLE, Structure.LIST, Structure.BAB_TITLE],
        law,
        0
    ) == True

    assert is_start_of_any(
        [Structure.LIST, Structure.BAB_TITLE],
        law,
        0
    ) == False


def test_is_start_of_structure():
    law = [
        'BAB X',
        'GUGATAN KE PENGADILAN',
        'Pengajuan gugatan dilakukan...'
    ]

    assert is_start_of_structure(Structure.BAB_NUMBER, law, 0) == True
    assert is_start_of_structure(Structure.UU_TITLE_TOPIC, law, 0) == False


def test_get_next_list_index():
    assert get_next_list_index('1.') == '2.'
    assert get_next_list_index('(1)') == '(2)'
    assert get_next_list_index('a.') == 'b.'
    with pytest.raises(Exception):
        get_next_list_index('Dengan adanya')


def test_get_squashed_list_item():
    assert get_squashed_list_item('nasi goreng; 3. bakmie ayam;') == 13
    assert get_squashed_list_item('gado-gado; dan/atau j. kue lapis;') == 20
    # From UU 13 2003 Ketenagakerjaan [Pasal 1, list index 27]
    assert get_squashed_list_item(
        'Siang berakhir pukul 18.00. 28. 1 hari adalah waktu selama 24 jam.') == 28


def test_clean_maybe_list_item():
    simple = '(1) Setiap Orang berhak memperoleh Informasi Publik.'
    assert clean_maybe_list_item(simple) == [
        '(1)',
        'Setiap Orang berhak memperoleh Informasi Publik.',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    true_positive_squashed = '(1) Setiap Orang berhak dilindungi hak-hak dasar. (2) Hak-hak yang dimaksud termasuk:'
    assert clean_maybe_list_item(true_positive_squashed) == [
        '(1)',
        'Setiap Orang berhak dilindungi hak-hak dasar.',
        '(2)',
        'Hak-hak yang dimaksud termasuk:'
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    false_positive_squashed = '(1) Calon anggota sebagaimana dimaksud dalam Pasal 3 ayat(2) diajukan oleh Presiden.'
    assert clean_maybe_list_item(false_positive_squashed) == [
        '(1)',
        'Calon anggota sebagaimana dimaksud dalam Pasal 3 ayat(2) diajukan oleh Presiden.',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    true_positive_squashed_first = 'Informasi yang wajib disediakan adalah: a. asas dan tujuan'
    assert clean_maybe_list_item(true_positive_squashed_first) == [
        'Informasi yang wajib disediakan adalah:',
        'a.',
        'asas dan tujuan',
    ]

    # From UU 14 2008 Keterbukaan Informasi Publik
    false_positive_squashed_first = 'Informasi yang wajib disediakan adalah asas dan tujuan'
    assert clean_maybe_list_item(false_positive_squashed_first) == [
        'Informasi yang wajib disediakan adalah asas dan tujuan',
    ]

    # From UU 13 2003 Ketenagakerjaan [Pasal 1, list index 27]
    true_positive_squashed = 'Siang berakhir pukul 18.00. 28. 1 hari adalah waktu selama 24 jam.'
    assert clean_maybe_list_item(true_positive_squashed) == [
        'Siang berakhir pukul 18.00.',
        '28.',
        '1 hari adalah waktu selama 24 jam.'
    ]

    # From UU 13 2003 Ketenagakerjaan [Pasal 79, list index 1]
    true_positive_squashed_multiple_whitespace = 'Pengusaha wajib memberi cuti kepada pekerja.  (2) Waktu istirahat dan cuti sebagaimana'
    assert clean_maybe_list_item(true_positive_squashed_multiple_whitespace) == [
        'Pengusaha wajib memberi cuti kepada pekerja.',
        '(2)',
        'Waktu istirahat dan cuti sebagaimana'
    ]