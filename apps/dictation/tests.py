"""Dictation tests."""

import pytest
from .contraction import lengthen_sentence

Q1 = "He'd come if he could."
Q2 = "I'd have helped him if he'd asked me."
Q3 = "He'd rather walk than run."
Q4 = "He'd gone home."
Q5 = "You'd better be careful - it might be dangerous."
Q6 = "He didn't know what to say."
Q7 = "She'll be here in ten minutes."
Q8 = "You aren't going to wear that jacket are you?"
Q9 = "It's the first time I have been ice skating."
Q10 = "We're watching a movie this evening."
Q11 = "If you'd been there, you'd have laughed."
Q12 = "The car's parked in the wrong place."
Q13 = "I'd better check on the children."
Q14 = "Aren't you going to the dance?"
Q15 = "This is Nick's car. No it isn't. This one's my teacher's."
Q16 = "They'll be arriving next week's visit."
Q17 = "His wife's son was now in school."
Q18 = "The brown fox jumped over the lazy dog's bone."
Q19 = "We haven't seen that movie yet."
Q20 = "The boys found the woman's keys."
Q21 = "The manager's boss is in a bad mood today."
Q22 = "Be careful with her cat's claws when you hold him."
Q23 = "That's the dog's toy."
Q24 = "Her friend Kate's going to the movies tonight."
Q25 = "I think that you should see your doctor's office."
Q26 = "We went into Jane' room to read her books' titles."
Q27 = "I can't promise anything, but I'll do what I can"
Q28 = "The children's friends are coming over to play soon."
Q29 = "My nephews' games are kept in the attic at my mum's house."
Q30 = "It was only the children's toys that were damaged in the fire."
Q31 = "Bob and Mona's house is bigger than mine."
Q32 = "I went to my cousin's house."
Q33 = "Chris's bike had a broken chain, so I borrowed Sam's bike."
Q34 = "The teams' achievement was great."
Q35 = "My dog's been buried there for five years now."
Q36 = "The cat's bowl is empty."
Q37 = "Lisa's iPod is broken."
Q38 = "We need the car's insurance."
Q39 = "My dad wouldn't let me drive his car."
Q40 = "Did you know his sisters' names?"
Q41 = "It was better than another woman's story."
Q42 = "I lost my new friend's car keys."
Q43 = "If she'd read Tim's book, she'd be able to sum it up."
Q44 = "They're doing an exercise for this semester's final exams."
Q45 = "My daughter's cookies were devoured in a minute or two at the party!"
Q46 = "What's happened?"
Q47 = "Don't refer to them as it's, they're just its."
Q48 = "The player with broken legs couldn't play."
Q49 = "Couldn't James use his cell phone because his battery had gone flat."
Q50 = "I'll keep my eye on his brother."
Q51 = "If you're going to be my doctor, I expect you to call me by my first name."
Q52 = "That's not Kevin's dog, its Masons."
Q53 = "Let's see, if we can get there by 11 o'clock."
Q54 = "If it'd cost less, she'd have bought more copies."
Q55 = "Sally couldn't come because she had to work for her Mum."
Q56 = "Here's what I'd like you to do."
Q57 = "I'm very shy around people I'm not familiar with."
Q58 = "There's a comma after happy hour."
Q59 = "We've been invited to a party at their place."
Q60 = "Why won't she move?"
Q61 = "No I won't!"
Q62 = "My friend's going to school next year."
Q63 = "Your mother's been telling stories about you all day now"
Q64 = "She'd already lied."
Q65 = "It's hotter than yesterday!"
Q66 = "It's a bit like a journey to another world, isn't it?"
Q67 = "Here's the book you asked for."
Q68 = "Paul's had a lot of trouble, but now, he's living peacefully."
Q69 = "He wasn't at the party."
Q70 = "My mother's working in her study. Don't make a noise..."
Q71 = "It's just a two days' trip... Don't take too many things with you!"
Q72 = "As she's a surgeon, she's a very busy woman."
Q73 = "When she really needed him, he'd helped her before she'd even asked."
Q74 = "When I arrived, she'd been in my office for two hours."
Q75 = "Don't worry. I've got a pretty good sense of direction."
Q76 = "Won't you come to the movies with me?"
Q77 = "I'm reading."
Q78 = "I'm reading, right now."
Q79 = "If we don't address age at menopause or reproductive span in"

A1 = "He would come if he could."
A2 = "I would have helped him if he had asked me."
A3 = "He would rather walk than run."
A4 = "He had gone home."
A5 = "You had better be careful - it might be dangerous."
A6 = "He did not know what to say."
A7 = "She will be here in ten minutes."
A8 = "You are not going to wear that jacket are you?"
A9 = "It is the first time I have been ice skating."
A10 = "We are watching a movie this evening."
A11 = "If you had been there, you would have laughed."
A12 = "The car is parked in the wrong place."
A13 = "I had better check on the children."
A14 = "Are you not going to the dance?"
A15 = "This is Nick's car. No it is not. This one is my teacher's."
A16 = "They will be arriving next week's visit."
A17 = "His wife's son was now in school."
A18 = "The brown fox jumped over the lazy dog's bone."
A19 = "We have not seen that movie yet."
A20 = "The boys found the woman's keys."
A21 = "The manager's boss is in a bad mood today."
A22 = "Be careful with her cat's claws when you hold him."
A23 = "That is the dog's toy."
A24 = "Her friend Kate is going to the movies tonight."
A25 = "I think that you should see your doctor's office."
A26 = "We went into Jane' room to read her books' titles."
A27 = "I cannot promise anything, but I will do what I can"
A28 = "The children's friends are coming over to play soon."
A29 = "My nephews' games are kept in the attic at my mum's house."
A30 = "It was only the children's toys that were damaged in the fire."
A31 = "Bob and Mona's house is bigger than mine."
A32 = "I went to my cousin's house."
A33 = "Chris's bike had a broken chain, so I borrowed Sam's bike."
A34 = "The teams' achievement was great."
A35 = "My dog has been buried there for five years now."
A36 = "The cat's bowl is empty."
A37 = "Lisa's iPod is broken."
A38 = "We need the car's insurance."
A39 = "My dad would not let me drive his car."
A40 = "Did you know his sisters' names?"
A41 = "It was better than another woman's story."
A42 = "I lost my new friend's car keys."
A43 = "If she had read Tim's book, she would be able to sum it up."
A44 = "They are doing an exercise for this semester's final exams."
A45 = "My daughter's cookies were devoured in a minute or two at the party!"
A46 = "What has happened?"
A47 = "Do not refer to them as it is, they are just its."
A48 = "The player with broken legs could not play."
A49 = "Could not James use his cell phone because his battery had gone flat."
A50 = "I will keep my eye on his brother."
A51 = "If you are going to be my doctor, I expect you to call me by my first name."
A52 = "That is not Kevin's dog, its Masons."
A53 = "Let us see, if we can get there by 11 o'clock."
A54 = "If it had cost less, she would have bought more copies."
A55 = "Sally could not come because she had to work for her Mum."
A56 = "Here is what I would like you to do."
A57 = "I am very shy around people I am not familiar with."
A58 = "There is a comma after happy hour."
A59 = "We have been invited to a party at their place."
A60 = "Why will she not move?"
A61 = "No I will not!"
A62 = "My friend is going to school next year."
A63 = "Your mother has been telling stories about you all day now"
A64 = "She had already lied."
A65 = "It is hotter than yesterday!"
A66 = "It is a bit like a journey to another world, is not it?"
A67 = "Here is the book you asked for."
A68 = "Paul has had a lot of trouble, but now, he is living peacefully."
A69 = "He was not at the party."
A70 = "My mother is working in her study. Do not make a noise..."
A71 = "It is just a two days' trip... Do not take too many things with you!"
A72 = "As she is a surgeon, she is a very busy woman."
A73 = "When she really needed him, he had helped her before she had even asked."
A74 = "When I arrived, she had been in my office for two hours."
A75 = "Do not worry. I have got a pretty good sense of direction."
A76 = "Will you not come to the movies with me?"
A77 = "I am reading."
A78 = "I am reading, right now."
A79 = "If we do not address age at menopause or reproductive span in"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (Q1, A1),
        (Q2, A2),
        (Q3, A3),
        (Q4, A4),
        (Q5, A5),
        (Q6, A6),
        (Q7, A7),
        (Q8, A8),
        (Q9, A9),
        (Q10, A10),
        (Q11, A11),
        (Q12, A12),
        (Q13, A13),
        (Q14, A14),
        (Q15, A15),
        (Q16, A16),
        (Q17, A17),
        (Q18, A18),
        (Q19, A19),
        (Q20, A20),
        (Q21, A21),
        (Q22, A22),
        (Q23, A23),
        (Q24, A24),
        (Q25, A25),
        (Q26, A26),
        (Q27, A27),
        (Q28, A28),
        (Q29, A29),
        (Q30, A30),
        (Q31, A31),
        (Q32, A32),
        (Q33, A33),
        (Q34, A34),
        (Q35, A35),
        (Q36, A36),
        (Q37, A37),
        (Q38, A38),
        (Q39, A39),
        (Q40, A40),
        (Q41, A41),
        (Q42, A42),
        (Q43, A43),
        (Q44, A44),
        (Q45, A45),
        (Q46, A46),
        (Q47, A47),
        (Q48, A48),
        (Q49, A49),
        (Q50, A50),
        (Q51, A51),
        (Q52, A52),
        (Q53, A53),
        (Q54, A54),
        (Q55, A55),
        (Q56, A56),
        (Q57, A57),
        (Q58, A58),
        (Q59, A59),
        (Q60, A60),
        (Q61, A61),
        (Q62, A62),
        (Q63, A63),
        (Q64, A64),
        (Q65, A65),
        (Q66, A66),
        (Q67, A67),
        (Q68, A68),
        (Q69, A69),
        (Q70, A70),
        (Q71, A71),
        (Q72, A72),
        (Q73, A73),
        (Q74, A74),
        (Q75, A75),
        (Q76, A76),
        (Q77, A77),
        (Q78, A78),
        (Q79, A79),
    ],
)
def test_lengthen_sentence(test_input, expected):
    """Test if the expected is without contraction and right."""
    if isinstance(test_input, tuple):
        test_input = test_input[0]
    if isinstance(expected, tuple):
        expected = expected[0]
    lengthened = lengthen_sentence(test_input)
    assert lengthened == expected
