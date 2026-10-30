from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..services.ai import generate_ai_recoms, generate_summary

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
    responses={404: {"description": "Not found"}},
)


@router.get("/summary/{movie_id}", description="AI generated Summary via movie_id.")
async def get_summary(movie_id: int) -> str:
    return StreamingResponse(generate_summary(movie_id), media_type="text/plain")


@router.get("/recommend/{movie_id}", description="AI recommendations for movie.")
def get_ai_recommendaions(movie_id: int):
    # return generate_ai_recoms(movie_id)
    return {
        "movie_id": 272,
        "movie_title": "Batman Begins",
        "candidates": {
            "155": [
                "The Dark Knight",
                "batman rais the stake in hi war on crime . with the help of lt. jim gordon and district attorney harvey dent , batman set out to dismantl the remain crimin organ that plagu the street . the partnership prove to be effect , but they soon find themselv prey to a reign of chao unleash by a rise crimin mastermind known to the terrifi citizen of gotham as the joker . action thriller crime sadism chao secretident crimefight superhero antihero scarecrow basedoncom vigilant organizedcrim tragichero antivillain criminalmastermind districtattorney superpow supervillain neo-noir bold christianbal heathledg aaroneckhart christophernolan",
            ],
            "268": [
                "Batman",
                "have wit hi parent ' brutal murder as a child , millionair philanthropist bruce wayn fight crime in gotham citi disguis as batman , a costum hero who strike fear into the heart of villain . but when a deform madman known as ' the joker ' seiz control of gotham 's crimin underworld , batman must face hi most ruthless nemesi ever while protect both hi ident and hi love interest , report vicki vale . fantasi action crime dualident doublelif chemic crimefight superhero villain basedoncom vigilant mobster organizedcrim crimin superpow mad vigilant cautionari goodversusevil michaelkeaton jacknicholson kimbasing timburton",
            ],
            "49026": [
                "The Dark Knight Rises",
                "follow the death of district attorney harvey dent , batman assum respons for dent 's crime to protect the late attorney 's reput and is subsequ hunt by the gotham citi polic depart . eight year later , batman encount the mysteri selina kyle and the villain bane , a new terrorist leader who overwhelm gotham 's finest . the dark knight resurfac to protect a citi that ha brand him an enemi . action crime drama thriller airplan fight burglar hostag secretident crimefight superhero villai timebomb basedoncom cover-up vigilant tragichero mobil terror destruct fight criminalunderworld catburglar flood christianbal garyoldman tomhardi christophernolan",
            ],
        },
        "ranked_candidates": {
            "ranked_candidates": [
                {
                    "rank": 1,
                    "tmdb_id": 155,
                    "title": "The Dark Knight",
                    "reason": "It is the direct sequel to Batman Begins, featuring the same director, lead actor, and building on the established gritty, realistic crime thriller tone.",
                },
                {
                    "rank": 2,
                    "tmdb_id": 49026,
                    "title": "The Dark Knight Rises",
                    "reason": "Also a direct sequel in Christopher Nolan's trilogy, continuing the narrative and character arcs established in the first film.",
                },
                {
                    "rank": 3,
                    "tmdb_id": 268,
                    "title": "Batman",
                    "reason": "While it shares the same core character and genre, it differs significantly in director, style, and tone compared to the grounded approach of the input film.",
                },
            ]
        },
    }
